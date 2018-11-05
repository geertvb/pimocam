from gpiozero import MotionSensor
from picamera import PiCamera
from picamera import PiCameraCircularIO
from picamera.frames import PiVideoFrameType

# Pin numbers
MOTION_PIN = 4


class PiMoCamCircularIO(PiCameraCircularIO):

    def __init__(self, camera, size=None, seconds=None, bitrate=17000000, splitter_port=1):
        super(PiMoCamCircularIO, self).__init__(camera, size, seconds, bitrate, splitter_port);

    def find_span(self, seconds, first_frame=PiVideoFrameType.sps_header):
        first = None
        last = None
        seconds = int(seconds * 1000000)
        for frame in reversed(self.frames):
            if first_frame in (None, frame.frame_type):
                first = frame
            if frame.timestamp is not None:
                if last is None:
                    last = frame
                elif last.timestamp - frame.timestamp >= seconds:
                    break
        return first, last


class PiMoCam:

    def __init__(self, pin=MOTION_PIN, record_before=30, record_after=20):
        self.pin = pin
        self.record_before = record_before
        self.record_after = record_after
        self.buffer_size = record_before + record_after + 10
        self.current_file = None
        self.last_motion = None
        self.last_frame = None
        self.pir = None
        self.camera = None

    def motion_started(self):
        print("Motion started")
        self.last_motion = None
        if self.current_file is not None:
            self.start_saving()

    def motion_finished(self):
        print("Motion finished")
        self.last_motion = 123

    def start_saving(self):
        print("Start saving")

    def init_pir(self):
        print("Init PIR")
        self.pir = MotionSensor(self.pin)
        self.pir.when_motion = self.motion_started
        self.pir.when_no_motion = self.motion_finished

    def cleanup_pir(self):
        print ("Cleanup PIR")
        self.pir.when_motion = None
        self.pir.when_no_motion = None
        self.pir = None

    def init_camera(self):
        print ("Init camera")
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        self.stream = PiMoCamCircularIO(self.camera, seconds=self.buffer_size)
        self.camera.start_recording(self.stream, format='h264')

    def cleanup_camera(self):
        print ("Cleanup camera")
        self.camera.stop_recording()

    def start(self):
        print ("Start")
        self.init_camera()
        self.init_pir()

    def wait(self, seconds=1):
        self.camera.wait_recording(seconds)

    def stop(self):
        print ("Stop")
        self.cleanup_pir()
        self.cleanup_camera()

    def find_span(self):
        print ("Find span")
        first, last = self.stream.find_span(5)
        print("first: {}".format(first))
        print("last: {}".format(last))


def main():
    print("Hello PiMoCam!")
    pimocam = PiMoCam()
    try:
        pimocam.start()
        while True:
            print('Recording ...')
            pimocam.wait(1)
            pimocam.find_span()
            # sleep(1)
    finally:
        print("Stop recording")
        pimocam.stop()


if __name__ == "__main__":
    main()
