import can
import time

def receive_can_messages():

    # 캔 인터페이스 설정 (예: can-0)
    can_interface = 'can0'
    
    # 캔 버스 열기
    bus = can.interface.Bus(channel=can_interface, bustype='socketcan')

    try:
        while True:
            # 메시지 수신 대기
            message = bus.recv()
            
            # 수신된 메시지 출력
            print(f"Received CAN message - ID: {message.arbitration_id}, Data: {message.data}")

    except KeyboardInterrupt:
        print("\nCAN Receiver terminated.")

if __name__ == "__main__":
    receive_can_messages()
print('hello world')
