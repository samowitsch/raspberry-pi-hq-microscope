import picamera
from PIL import Image, ImageFont, ImageDraw 
import RPi.GPIO as GPIO
import time
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("advanced.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 180
camera.framerate = 30
camera.start_preview()


img = Image.open('overlay.png')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
draw.text((10, 5), "RPI MICRO TEST", font=font, align ="left")

pad = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))

pad.paste(img, (0, 0))

o = camera.add_overlay(pad.tobytes(), size=img.size, layer=3, alpha = 254)
#camera.remove_overlay(o)

# gpio buttons of the pcb adapter board
BTN_MODE = 17
BTN_INCREASE = 27
BTN_DECREASE = 22
BTN_CAPTURE = 19
BTN_SHUTDOWN = 26

PATH_CAPTURE = "/home/micro/"

GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_MODE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_INCREASE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_DECREASE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_CAPTURE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def mode_select(channel):
    logging.info("Pressed mode")
    time.sleep(1)

def increase(channel):
    logging.info("Increase value")
    time.sleep(1)

def decrease(channel):
    logging.info("Decrease value")
    time.sleep(1)

def capture_photo(channel):
    logging.info("Capture photo")
    t = time.localtime()
    filename = "capture" + time.strftime('-%Y-%m-%d_%H-%M-%S', t) + ".jpg"
    camera.capture(PATH_CAPTURE+filename)

    # owner:group can vary depending to in sd card setup given username
    os.system("chown micro:micro " + filename)

def shutdown(channel):
    logging.info("Shutting down")
    time.sleep(1)
    os.system("sudo shutdown -h now")

GPIO.add_event_detect(BTN_MODE, GPIO.FALLING, callback=mode_select, bouncetime=1100)
GPIO.add_event_detect(BTN_INCREASE, GPIO.FALLING, callback=increase, bouncetime=1100)
GPIO.add_event_detect(BTN_DECREASE, GPIO.FALLING, callback=decrease, bouncetime=1100)
GPIO.add_event_detect(BTN_CAPTURE, GPIO.FALLING, callback=capture_photo, bouncetime=1100)
GPIO.add_event_detect(BTN_SHUTDOWN, GPIO.FALLING, callback=shutdown, bouncetime=1100)

logging.info("Advanced script started")
while 1:
    time.sleep(1)