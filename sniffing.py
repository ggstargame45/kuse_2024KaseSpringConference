import can
# CAN 인터페이스 설정 (실제 인터페이스 이름에 맞게 수정)
can_interface = 'can0'
# CAN 버스 생성
bus = can.interface.Bus(channel=can_interface, bustype='socketcan')
try:
# 무한 루프를 통해 CAN 데이터 수신
	while True:
		message = bus.recv(timeout=1.0) # timeout은 초 단위로 조절 가능
		if message is not None:
# 수신된 CAN 메시지의 ID와 데이터 출력
			can_data = [hex(i) for i in message.data]			
			print(f"ID: {hex(message.arbitration_id)}, Data: {can_data}")
except KeyboardInterrupt:
# Ctrl+C를 눌렀을 때 프로그램 종료
	print("프로그램을 종료합니다.")
finally:
# 프로그램 종료 시 CAN 버스 닫기
	bus.shutdown()
