import machine
import sys
import select

# LED 핀 설정 (선생님이 가진 LED 연결에 맞게 GP 번호 수정 가능)
led_red = machine.Pin(14, machine.Pin.OUT)
led_green = machine.Pin(15, machine.Pin.OUT)
led_blue = machine.Pin(16, machine.Pin.OUT)

# 모든 LED 끄기 함수
def all_off():
    led_red.value(0)
    led_green.value(0)
    led_blue.value(0)

# 시작 시 LED 초기화
all_off()

# 시리얼 입력을 감시하기 위한 select 객체 생성
poll_object = select.poll()
poll_object.register(sys.stdin, select.POLLIN)

print("Pico Ready...") # 연결 확인용 메시지

while True:
    # 시리얼 포트에 데이터가 들어왔는지 확인 (대기 시간 10ms)
    if poll_object.poll(10):
        # 한 줄 읽어오기 (끝의 공백/줄바꿈 제거)
        command = sys.stdin.readline().strip()
        
        if command == "R":    # 가위 인식 시
            all_off()
            led_red.value(1)  # 빨간색 켜기
        elif command == "G":  # 바위 인식 시
            all_off()
            led_green.value(1)# 초록색 켜기
        elif command == "B":  # 보 인식 시
            all_off()
            led_blue.value(1) # 파란색 켜기
        elif command == "O":  # 인식 불가능 시
            all_off()