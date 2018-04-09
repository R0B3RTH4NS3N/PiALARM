#!/usr/bin/python3

# *** PiALARM by Robert Hansen ***

import RPi.GPIO as GPIO
import time, os
from tplight import LB130
import simpleaudio as sa

#
waketime = "07:00"
#

#set up tplight

while True:
	try:
		light = LB130("192.168.0.2")
		lightON = True
		break
	except Exception:
		print("ERROR -> connection to bulb not possible")
		time.sleep(1)

#set up GPIO

led = 11
button = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(led, GPIO.OUT) #warning: already in use?!
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(led, GPIO.LOW)

#set up simpleaudio

wave_obj = sa.WaveObject.from_wave_file("/home/pi/PiALARM/WoodenSailingShipOnSea.wav")
play_obj = wave_obj.play()
time.sleep(5)
play_obj.stop()

#endless loop

print("PiALARM is activated")

try:
	while True:
		ctime = time.strftime("%H:%M:%S")
		if ctime == ( waketime + ":00" ):
			GPIO.output(led, GPIO.HIGH)
			wave_obj = sa.WaveObject.from_wave_file("/home/pi/PiALARM/WoodenSailingShipOnSea.wav")
			play_obj = wave_obj.play()
			if not lightON:
				light.on()
				lightON = True
		if GPIO.input(button):
			GPIO.output(led, GPIO.LOW)
			if play_obj.is_playing():
				play_obj.stop()
			if lightON:
				light.off()
				lightON = False
				time.sleep(1)
			else:
				light.on()
				lightON = True
				time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
	light.on()
