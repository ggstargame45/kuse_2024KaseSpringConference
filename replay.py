import can
import time

bus=can.interface.Bus(channel='can0',bustype='socketcan')

message_id=0x123
rec_data=[0,0,0,0,0,0,0,0]
def repeat(id,data):
	msg=can.Message(arbitration_id=id,data=data,is_extended_id=False)
	bus.send(msg)
	time.sleep(1)


while True:
	rec_bus=bus.recv()
	
	if rec_bus.data[6]<5:
		message_id=rec_bus.arbitration_id
		rec_data[6]=rec_bus.data[6]
		break


while True:
	repeat(message_id,rec_data)
