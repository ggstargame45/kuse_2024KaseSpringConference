import can

can_interface = 'can0'
bus = can.interface.Bus(channel=can_interface, bustype='socketcan')

print(f"Receiving messages on {can_interface}...")

def diffie_hellman(prime, generator, private_key):
    public_key = pow(generator, private_key, prime)
    return public_key

# node2의 정보
node2_private_key = 6
node2_prime = 23
node2_generator = 5

try:
    while True:
        message = bus.recv()
        if message.arbitration_id == 0x123: # 수신된 메시지의 ID 확인
            received_key = int.from_bytes(message.data, byteorder='little')
            print("Received Public Key from Arduino:", received_key)
            
            node2_public_key = diffie_hellman(node2_prime, node2_generator, node2_private_key)
            print("Node2's Public Key:", node2_public_key)
            
            final_key = diffie_hellman(node2_prime, received_key, node2_private_key)
            print("Shared Key:", final_key)
except KeyboardInterrupt:
    print("\nExiting...")
