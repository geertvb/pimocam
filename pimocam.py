from gpiozero import MotionSensor
from time import sleep
from signal import pause
import picamera

# Pin numbers
MOTION_PIN = 4

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
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)
        self.stream = picamera.PiCameraCircularIO(self.camera, seconds = self.buffer_size)
        self.camera.start_recording(self.stream, format='h264')

    def cleanup_camera(self):
        print ("Cleanup camera")
        self.camera.stop_recording()

    def start(self):
        print ("Start")
        # self.init_camera()
        self.init_pir()

    def wait(self, seconds=1):
        self.camera.wait_recording(seconds)

    def stop(self):
        print ("Stop")
        self.cleanup_pir()
        # self.cleanup_camera()

def main():
    print("Hello PiMoCam!")
    pimocam = PiMoCam()
    try:
        pimocam.start()
        while True:
            print('Recording ...')
            # pimocam.wait()
            sleep(1)
    finally:
        print("Stop recording")
        pimocam.stop()


if __name__ == "__main__":
    main()
