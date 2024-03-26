import can
import time

# CAN interface set
interface = 'can0'

# open can bus
bus = can.interface.Bus(channel=interface, bustype='socketcan')

# list = can message for replay

replay_messages = [
	can.Message(arbitration_id=0x123, data=[0x01,0x02,0x03]),
	can.Message(arbitration_id=0x456, data=[0x04,0x05,0x06]),
	# add the additional message
]

try:
	while True:
		for msg in replay_messages:
			bus.send(msg)
			time.sleep(0.1)

except KeyboardInterrupt:

	print("Relpay terminated.")
