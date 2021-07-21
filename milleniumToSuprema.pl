use Date::Manip;
use File::Basename;
use Text::CSV;
use Getopt::Long;

## Millenium Columns
$employeeID         = 'Employee ID';            # 32
$firstName          = 'First Name';             # Joe
$lastName           = 'Last Name';              # Doe
$card1FacilityCode  = 'Card 1 Facility Code';   # 100
$card1Number        = 'Card 1 Encoded Card No.';# 10164
$card1Active        = 'Card 1 Active';          # True
$card1Activation    = 'Card 1 Activation Date'; # 3/13/2019 12:00:00 AM
$card1Expiration    = 'Card 1 Expiration Date'; # 1/1/2150 12:00:00 AM

my $file; 
my $biostar2LookupFl;
GetOptions('m=s' => \$file, 'b=s' => \$biostar2LookupFl);

$now                = ParseDate("now");
$fmtNow             = UnixDate($now,"%Y%m%d");
$base               = basename($file, ".csv");
$fileInactive       = qq(${base}.${fmtNow}.inactive.csv);
$fileExpired        = qq(${base}.${fmtNow}.expired.csv);
$fileSameNames      = qq(${base}.${fmtNow}.sameNames.csv);
$inactiveCnt        = 0;
$expiredCnt         = 0;
$cntNames           = 0;
$totalNames         = 0;
my $csv             = Text::CSV->new ({ binary => 1, auto_diag => 1 });
%lookup             = &parseBiostar2Lookup($biostar2LookupFl);
$maxBiostar2Date    = ParseDate("12/31/2030 23:59:59");
$ymdBiostar2MDate   = UnixDate($maxBiostar2Date,"%Y-%m-%d %T");

open my $fh, "<", $file or die "$file: $!";
while (my $row = $csv->getline ($fh)) {
    my @col = @$row;
    if ($i==0) { # header: column names
        $header = $row;
        for $j (0..$#col) { 
            $hashIndCol{$j} = $col[$j];
            $hashColInd{$col[$j]} = $j;
        }
        #for $k (sort {$a <=> $b} keys %hashIndCol) { print qq($k => $hashIndCol{$k}\n);}
    } else {
        $line = $row;
        $isCardActive = $col[$hashColInd{$card1Active}];
        if ($isCardActive eq "True") { # active card 1
            $startDate      = ParseDate($col[$hashColInd{$card1Activation}]);
            $endDate        = ParseDate($col[$hashColInd{$card1Expiration}]);

            if  (   (!&trim($endDate)) || # will print a record for tenants for which card1 expired
                    (&trim($endDate) && ($now gt $endDate))
                ) {
                if ($expiredCnt==0) { # store expired records in a file for review
                    open $fhe, ">:encoding(utf8)", "${fileExpired}" or die "cannot write into ${fileExpired} $!";
                    $csv->say ($fhe, $header);
                }
                $csv->say ($fhe, $line);
                $expiredCnt++;
            }

            if (&trim($startDate) && &trim($endDate) && 
                    ($now ge $startDate && $now le $endDate)) # cards are active and dates are within range
            { 
                $emid           = $col[$hashColInd{$employeeID}];
                $fname          = $col[$hashColInd{$firstName}];
                $lname          = $col[$hashColInd{$lastName}];
                $name           = qq($fname $lname); 
                $card           = $col[$hashColInd{$card1FacilityCode}] . "-" . $col[$hashColInd{$card1Number}]; # wiegand format 100-12345  
                $sdate          = &UnixDate($startDate, "%Y-%m-%d %T");
                $edate          = &UnixDate($endDate, "%Y-%m-%d %T");
                
                $card2          = ($col[$hashColInd{'Card 2 Encoded Card No.'}]) 
                                    ? $col[$hashColInd{'Card 2 Facility Code'}] . "-" . $col[$hashColInd{'Card 2 Encoded Card No.'}] : "";
                $sdate2         = &UnixDate($col[$hashColInd{'Card 2 Activation Date'}],"%Y-%m-%d %T");
                $edate2         = &UnixDate($col[$hashColInd{'Card 2 Expiration Date'}],"%Y-%m-%d %T");
                $card3          = ($col[$hashColInd{'Card 3 Encoded Card No.'}]) 
                                    ? $col[$hashColInd{'Card 3 Facility Code'}] . "-" . $col[$hashColInd{'Card 3 Encoded Card No.'}] : "";
                $sdate3         = &UnixDate($col[$hashColInd{'Card 3 Activation Date'}],"%Y-%m-%d %T");
                $edate3         = &UnixDate($col[$hashColInd{'Card 3 Expiration Date'}],"%Y-%m-%d %T");

                # only names are found to have dupes (no dupes for cards or employee ids)
                push(@{$hashName{$name}},qq($emid,"$fname","$lname",$card,$sdate,$edate,$card2,$sdate2,$edate2,$card3,$sdate3,$edate3));
                
                $fmtSdate = ($startDate gt $maxBiostar2Date) ? $ymdBiostar2MDate : $sdate;
                $fmtEdate = ($endDate gt $maxBiostar2Date) ? $ymdBiostar2MDate : $edate;

                if (!(exists $lookup{$emid})) { # new users - not found in biostar 2 but found in millenium
                    $newUsersHash{$emid} = qq($emid,"$name",$fmtSdate,$fmtEdate,$card);
                } else { # users are both in millenium and biostar 2
                    if ($lookup{$emid}->[2] ne $name) { # however, for the same employee id, name in biostar 2 and millenium are different
                        $updatedUsersHash{$emid} = qq($emid,"$name",$fmtSdate,$fmtEdate,$card);
                    }
                }
                
            }
        } else { # show inactive card 1 records 
            if ($inactiveCnt==0) { # store inactive records in a file for review
                open $fhi, ">:encoding(utf8)", "${fileInactive}" or die "cannot write into ${fileInactive} $!";
                $csv->say ($fhi, $header); #$csv->say ($fhi, $_) for @rows;
            }
            $csv->say ($fhi, $line);
            $inactiveCnt++;
        }
    }

    $i++;
}
close $fh;
close $fhi if ($inactiveCnt);
close $fhe if ($expiredCnt);

# same names getting duplicated
for $name (sort keys %hashName) { 
    @arr = @{$hashName{$name}};
    $totalNames++;
    if (scalar(@arr)>1) { # duplicates exist
        if ($cntNames == 0) { # store duplicates in separate file for review
            open FLN, qq(>${fileSameNames}) or die qq(Cannot create ${fileSameNames}: $!\n);
            print FLN qq(id,firstName,lastName,card1,startdate1,expdate1,card2,startdate2,expdate2,card3,startdate3,expdate3\n);
        }
        my $crdCnt = 1;
        for my $rec (@arr) {
            print FLN qq(${rec}\n);
            # update existing name field by appending card no, i.e. if name is "Joe Doe", update to "Joe Doe - C1"
            $csv->parse($rec);
            @col = $csv->fields();
            $emid = $col[0];
            $card = $col[3];
            $curName = qq("$col[1] $col[2]");
            $newName = qq("$col[1] $col[2] - C${crdCnt}");
            $fmtSdate = ( &ParseDate($col[4]) ge $maxBiostar2Date ) ? $ymdBiostar2MDate : $col[4];
            $fmtEdate = ( &ParseDate($col[5]) ge $maxBiostar2Date)  ? $ymdBiostar2MDate : $col[5];
            $modRec = qq($emid,$newName,$fmtSdate,$fmtEdate,$card);

            if (exists $newUsersHash{$emid}) { 
                #print qq(Replacing new rec <$newUsersHash{$emid}> with <$modRec>\n);    
                delete $newUsersHash{$emid};
            }
            if (exists $updatedUsersHash{$emid}) {
                #print qq(Replacing existing rec <$updatedUsersHash{$emid}> with <$modRec>\n);
                delete $updatedUsersHash{$emid};
                #print qq(upd $emid : Changed $curName to $newName [biostar: ) . $lookup{$emid}->[2] . qq(]\n);
            }
            #print qq(dup modified : $modRec\n); # qq($col[4] => ) . &ParseDate($col[4]) . qq(max=$maxBiostar2Date ;) . (&ParseDate($col[4]) ge $maxBiostar2Date) .
            $duplicates{$emid} = $modRec;
            $crdCnt++;
        }
        print FLN qq(\n);
        $cntNames++;
    }
}
close FLN if ($cntNames>0);

print qq(Total number of inactive accounts: $inactiveCnt out of $i\n)   if ($inactiveCnt);
print qq(Total number of expired accounts: $expiredCnt out of $i\n) if ($expiredCnt);
print qq(Same active names appearances: $cntNames out of $totalNames\n) if ($cntNames);

# create new users file in Biostar 2
&createBioStarFile(qq(biostar.new.${fmtNow}.csv),%newUsersHash);
# create updated list of users in Biostar 2
&createBioStarFile(qq(biostar.upd.${fmtNow}.csv),%updatedUsersHash);
# create duplicate list of users in Biostar 2
&createBioStarDupFile(qq(biostar.dup.${fmtNow}.csv),%duplicates);

sub createBioStarFile() { 
    my ($file, %hash) = @_;
    open FL, qq(>${file}) or die qq(cant create $file : $!\n);
    print FL qq(user_id,name,start_datetime,expiry_datetime,26 bit SIA Standard-H10301\n);
    for $key (sort keys %hash) { 
        print FL qq($hash{$key}\n);
        #print qq($hash{$key}\n);
    }
    close FL;
}

sub createBioStarDupFile() { 
    my ($file, %hash) = @_;
    open FL, qq(>${file}) or die qq(cant create $file : $!\n);
    print FL qq(user_id,name,start_datetime,expiry_datetime,26 bit SIA Standard-H10301\n);
    @sorted = sort { getName($hash{$a}) cmp getName($hash{$b})  } keys %hash;
    foreach my $rec (@sorted) {
        print FL qq($hash{$rec}\n);
    }
    close FL;
}

sub getName() { 
    my ($rec) = @_;
    $csv->parse($rec);
    return ($csv->fields())[1];
}

sub parseBiostar2Lookup() { 
    my ($file) = @_;
    my (%lookupHash);
    if (-f $file) {
        my $cnt = 0;
        open my $fh, "<", $file or die "$file: $!";
        while (my $row = $csv->getline ($fh)) {
            my @col = @$row;
            if ($cnt == 0) { 
                # header row
            } else { 
                $lookupHash{$col[1]} = $row; # eid
            }
            $cnt++;
        }
        close $fh;
    } else { 
        print qq(No Biostar2 lookup file found $file\n);
    }
    return %lookupHash;
}

sub trim() { 
    my ($s) = @_;
    ($t = $s) =~ (s/^\s*(.*?)\s*$/$1/g);
    return $t;
}