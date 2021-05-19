# https://stackoverflow.com/questions/60571501/how-to-rtsp-stream-a-video-using-gstreamer-and-python
# So, I ended up managing to make the link provided work. My problem was with the video's width and height, 
# which must have the exact same values as the video you want to play, maybe something to do with opencv frames passing...also, 
# the "is-live" property, which was set to true due to the use of webcam camera from the link's solution must be set to false 
# (or not used at all since that is the default value) or else the video will begin with a certain delay in black screen. 
# The code ended up being:

import cv2
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib #, GObject


class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        #self.cap = cv2.VideoCapture("/home/ielis/camera-test/test.mp4")
        self.cap = cv2.VideoCapture(0) # 0 - captures camera
        self.number_frames = 0
        self.fps = 30 #8
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        # 'caps=video/x-raw,format=BGR,width=640,height=480,framerate={}/1 ' \ - it must match camera resolution
        # 'caps=video/x-raw,format=BGR,width=1280,height=720,framerate={}/1 ' \
        # is-live=true (inserted after name=source works fine with webcam)
        self.launch_string = 'appsrc name=source block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width=640,height=480,framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ! queue ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96 '.format(self.fps)
        # streams to gst-launch-1.0 rtspsrc location=rtsp://localhost:8554/test latency=50 ! decodebin ! autovideosink

    def on_need_data(self, src, lenght):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                data = frame.tobytes() # frame.tostring() - deprecated
                #print(data)
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.number_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.number_frames += 1
                retval = src.emit('push-buffer', buf)
                #print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                #                                                                       self.duration,
                #                                                                       self.duration / Gst.SECOND))
                if retval != Gst.FlowReturn.OK:
                    print(retval)

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.get_mount_points().add_factory("/test", self.factory)
        self.attach(None)

#GObject.threads_init()
Gst.init(None)

server = GstServer()

#loop = GObject.MainLoop()
#loop.run()

main_loop = GLib.MainLoop()
main_loop.run()