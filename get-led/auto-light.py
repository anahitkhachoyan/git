import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
button = 6
GPIO.setup(button, GPIO.IN)
GPIO.input(button)
while True:
    GPIO.output(led,1-GPIO.input(button))
    time.sleep(0.1)
