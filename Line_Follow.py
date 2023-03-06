#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from TRSensors import TRSensor
import time

Button = 7
BUZ = 4
#30 (10+7+10+7-4)
path = ['EM','EL','EK','EJ','EI','EH','EG','EF','EE','FE','GE','HE','IE','JE','KE','KF','KG','KH','KI','KJ','KK','KL','KM','KN','JN','IN','HN','GN','FN','EN']
#GG GH GI GJ GK GL HL IL IK IJ II IH IG IG HG GG

def beep_on():
	GPIO.output(BUZ,GPIO.HIGH)
def beep_off():
	GPIO.output(BUZ,GPIO.LOW)



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(BUZ,GPIO.OUT)

maximum = 20
j = 0
integral = 0
last_proportional = 0
location=0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('35.201.145.28',12001))

TR = TRSensor()
Ab = AlphaBot2()
Ab.stop()
print("Line follow Example")
time.sleep(0.5)
for i in range(0,100):
	if(i<25 or i>= 75):
		Ab.right()
		Ab.setPWMA(30)
		Ab.setPWMB(30)
	else:
		Ab.left()
		Ab.setPWMA(30)
		Ab.setPWMB(30)
	TR.calibrate()
Ab.stop()
print(TR.calibratedMin)
print(TR.calibratedMax)
while (GPIO.input(Button) != 0):
	position,Sensors = TR.readLine()
	print(position,Sensors)
	time.sleep(0.05)
Ab.setPWMA(20)
Ab.setPWMB(20)
Ab.forward()

while True:
	try:
		if (GPIO.input(Button) == 0):
			#sucket end
			print("end")
		position,Sensors = TR.readLine()
		#print(position)
		if(Sensors[0] >820 and Sensors[1] >820 and Sensors[2] >820 and Sensors[3] >820 and Sensors[4] >820):
			Ab.forward
			print("------")
		if(Sensors[0] <780 and Sensors[1] <780 and Sensors[2] <780 and Sensors[3] <780 and Sensors[4] <780):
			Ab.setPWMA(10)
			Ab.setPWMB(10)
			beep_on()
			time.sleep(0.55)
			beep_off()
			msg="report "+path[location]+"/n"
			sock.send(bytes(msg))
			print(path[location])
			#
			rec=str(sock.recv(1024))
			if(rec=="avoid"):
				for i in range(0,60000):
					Ab.right()
					print("right")
				for i in range(0,60000):
					Ab.forward()
					print("forward")
				while(True):
					msg1="report "+path[location]+"/n"
					sock.send(bytes(msg1))
					rec1=str(sock.recv(1024))
					if(rec1=="can_go"):
						for i in range(0,60000):
							Ab.left()
						print("left")
						for i in range(0,60000):
							Ab.forward()
							print("forward")
						break
			if(rec=="wait"):
				Ab.stop()
				while(True):
					msg1="report "+path[location]+"/n"
					sock.send(bytes(msg1))
					rec1=str(sock.recv(1024))
					if(rec1=="can_go"):
						break
				
			
			if(location==8 or location==14 or location==23):
				Ab.stop()
				for i in range(0,24000):
					Ab.left()
					print("left")
				for i in range(0,60000):
					Ab.forward()
					print("forward")
				Ab.setPWMA(20)
				Ab.setPWMB(20)	
				Ab.forward()
			if(location==29):
				location=0
				Ab.stop()
				for i in range(0,12000):
					Ab.left()
					print("right")
				for i in range(0,300):
					Ab.forward()
					print("forward")
				Ab.setPWMA(20)
				Ab.setPWMB(20)	
				Ab.forward()
			location=location+1
		else:
			# The "proportional" term should be 0 when we are on the line.
			proportional = position - 2000
			
			# Compute the derivative (change) and integral (sum) of the position.
			derivative = proportional - last_proportional
			integral += proportional
			
			# Remember the last position.
			last_proportional = proportional

			power_difference = proportional/30  + integral/10000 + derivative*2;  

			if (power_difference > maximum):
				power_difference = maximum
			if (power_difference < - maximum):
				power_difference = - maximum
			if (power_difference < 0):
				Ab.setPWMA(maximum + power_difference)
				Ab.setPWMB(maximum)
			else:
				Ab.setPWMA(maximum)
				Ab.setPWMB(maximum - power_difference)
	except KeyboardInterrupt:
		break
