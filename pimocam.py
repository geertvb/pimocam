from gpiozero import MotionSensor
# from time import sleep
from signal import pause

pir = MotionSensor(4)

def motionStarted():
    print("Motion started")

def motionFinished():
    print("Motion finished")

pir.when_motion = motionStarted
pir.when_no_motion = motionFinished

def main():
    print("Hello PiMoCam!")
    # while True:
    #     sleep(1)
    #     print("Motion: {}".format(pir.motion_detected))
    pause()


if __name__ == "__main__":
    main()
