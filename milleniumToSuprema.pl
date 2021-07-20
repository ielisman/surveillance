use Date::Manip;
use File::Basename;
use Text::CSV;

## Millenium Columns
$employeeID         = 'Employee ID';            # 32
$firstName          = 'First Name';             # Joe
$lastName           = 'Last Name';              # Doe
$card1FacilityCode  = 'Card 1 Facility Code';   # 100
$card1Number        = 'Card 1 Encoded Card No.';# 10164
$card1Active        = 'Card 1 Active';          # True
$card1Activation    = 'Card 1 Activation Date'; # 3/13/2019 12:00:00 AM
$card1Expiration    = 'Card 1 Expiration Date'; # 1/1/2150 12:00:00 AM

$file               = shift;
$now                = ParseDate("now");
$base               = basename($file, ".csv");
$fileInactive       = qq(${base}.inactive.csv);
$fileExpired        = qq(${base}.expired.csv);
$fileSameNames      = qq(${base}.sameNames.csv);
$inactiveCnt        = 0;
$expiredCnt         = 0;
$cntNames           = 0;
$totalNames         = 0;
my $csv             = Text::CSV->new ({ binary => 1, auto_diag => 1 });

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
        if ($isCardActive eq "True") {
            $startDate      = ParseDate($col[$hashColInd{$card1Activation}]);
            $endDate        = ParseDate($col[$hashColInd{$card1Expiration}]);

            if  (   (!&trim($endDate)) || # will print a record for tenants for which card1 expired
                    (&trim($endDate) && ($now gt $endDate))
                ) {
                if ($expiredCnt==0) {
                    open $fhe, ">:encoding(utf8)", "${fileExpired}" or die "cannot write into ${fileExpired} $!";
                    $csv->say ($fhe, $header);
                }
                $csv->say ($fhe, $line);
                $expiredCnt++;
            }

            if (&trim($startDate) && &trim($endDate) && 
                    ($now ge $startDate && $now le $endDate)) 
            { 
                $emid           = $col[$hashColInd{$employeeID}];
                $fname          = $col[$hashColInd{$firstName}];
                $lname          = $col[$hashColInd{$lastName}];
                $name           = qq($fname $lname); 
                $card           = $col[$hashColInd{$card1FacilityCode}] . "-" . $col[$hashColInd{$card1Number}]; # wiegand format 100-12345  
                $sdate          = &UnixDate($startDate, "%Y%m%d");
                $edate          = &UnixDate($endDate, "%Y%m%d");
                
                $card2          = ($col[$hashColInd{'Card 2 Encoded Card No.'}]) 
                                    ? $col[$hashColInd{'Card 2 Facility Code'}] . "-" . $col[$hashColInd{'Card 2 Encoded Card No.'}] : "";
                $sdate2         = &UnixDate($col[$hashColInd{'Card 2 Activation Date'}],"%Y%m%d");
                $edate2         = &UnixDate($col[$hashColInd{'Card 2 Expiration Date'}],"%Y%m%d");
                $card3          = ($col[$hashColInd{'Card 3 Encoded Card No.'}]) 
                                    ? $col[$hashColInd{'Card 3 Facility Code'}] . "-" . $col[$hashColInd{'Card 3 Encoded Card No.'}] : "";
                $sdate3         = &UnixDate($col[$hashColInd{'Card 3 Activation Date'}],"%Y%m%d");
                $edate3         = &UnixDate($col[$hashColInd{'Card 3 Expiration Date'}],"%Y%m%d");

                push(@{$hashName{$name}},qq($emid,"$fname","$lname",$card,$sdate,$edate,$card2,$sdate2,$edate2,$card3,$sdate3,$edate3)); # only names are dupes (no dupes for cards or employee ids)
                $recHash{$emid} = qq($emid,"$name",$card,$sdate,$edate);
            }
        } else { # show inactive 1st cards 
            if ($inactiveCnt==0) {
                open $fhi, ">:encoding(utf8)", "${fileInactive}" or die "cannot write into ${fileInactive} $!";
                #$csv->say ($fhi, $_) for @rows;
                $csv->say ($fhi, $header);
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

for $name (sort keys %hashName) { 
    @arr = @{$hashName{$name}};
    $totalNames++;
    # in case of the same names, only retrieve records with latest end date
    if (scalar(@arr)>1) {
        if ($cntNames == 0) { 
            open FLN, qq(>${fileSameNames}) or die qq(Cannot create ${fileSameNames}: $!\n);
            print FLN qq(id,firstName,lastName,card1,startdate1,expdate1,card2,startdate2,expdate2,card3,startdate3,expdate3\n);
        }
        for my $rec (@arr) { 
            print FLN qq(${rec}\n);
        }
        print FLN qq(\n);
        $cntNames++;
    }
}
close FLN if ($cntNames>0);

print qq(Total number of inactive accounts: $inactiveCnt out of $i\n)   if ($inactiveCnt);
print qq(Total number of expired accounts: $expiredCnt out of $i\n) if ($expiredCnt);
print qq(Same active names appearances: $cntNames out of $totalNames\n) if ($cntNames);

sub trim() { 
    my ($s) = @_;
    ($t = $s) =~ (s/^\s*(.*?)\s*$/$1/g);
    return $t;
}