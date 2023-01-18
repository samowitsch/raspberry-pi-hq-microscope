import RPi.GPIO as GPIO
import time
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("shutdown.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

BTN_SHUTDOWN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdown(channel):
    logging.info("Shutting down")
    time.sleep(1)
    os.system("sudo shutdown -h now")

GPIO.add_event_detect(BTN_SHUTDOWN, GPIO.FALLING, callback=shutdown, bouncetime=1000)

logging.info("Shutdown script started")
while 1:
    time.sleep(1)
