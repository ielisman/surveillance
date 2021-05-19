from threading import Thread
from time import sleep

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstApp, GLib, GstRtspServer, GObject

_ = GstApp

Gst.init()

main_loop = GLib.MainLoop()
main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

#cmd = "ksvideosrc num-buffers=1 ! jpegenc ! filesink location=capture1.jpeg"
#cmd = "appsrc emit-signals=True is-live=True  caps=video/x-raw,format=RGB,width=640,height=480,framerate=30/1 ! queue max-size-buffers=4 ! videoconvert ! autovideosink"
# "ksvideosrc ! video/x-raw, width=640, height=480 ! decodebin ! videoconvert ! autovideosink") # ! appsink name=video")
cmd = "rtspsrc location=rtsp://localhost:8554/test latency=50 ! decodebin ! autovideosink"
pipeline = Gst.parse_launch(cmd) # ! appsink name=video")
#appsink = pipeline.get_by_name("video")
pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        #sample = appsink.try_pull_sample(Gst.SECOND)
        #if sample is None:
        #    continue
        #print("Got a sample ")
        sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()