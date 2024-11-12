import subprocess
import time
import re
import configparser
import os
import requests
from datetime import datetime
import csv
#import texture   # 자동 창 생성 때문에 함수안에 넣을거임
import threading

# x값 설정파일 읽어오기
config = configparser.ConfigParser()
config.read('config.ini')
# 설정파일에서 x값 가져오기
s_out = float(config['scale']['CPU_SCALE_OUT'])
s_in = float(config['scale']['CPU_SCALE_IN'])

# log 디렉토리 생성
log_directory = './scale_log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# log.csv 파일에 로그 저장하는 함수
def log_to_csv(cpu_usage, scale):
    log_file = os.path.join(log_directory, 'scale_log.csv')
    log_data = [f'time : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', f'cpu 사용량 : {cpu_usage}', scale]

    # CSV 파일에 추가 모드로 기록
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(log_data)

# 모니터링할 컨테이너의 이름 또는 ID
container_name = 'samdul-blog-1'  # 여기에 원하는 컨테이너 이름 또는 ID 입력

# Docker stats 명령어 실행 (특정 컨테이너만 모니터링)
command = ['docker', 'stats', container_name, '--format', 'table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}']

# subprocess.Popen을 사용하여 명령어 실행
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

print(f"{container_name} 컨테이너의 Docker stats 명령어 실행 중...")

scale_value = 1  # 스케일 값 초기화, 1은 이미 있음

cpu_up_time = 0
cpu_down_time = 0
check_time = 10

scale_check = False

# 수동 스케일 인/아웃 호출
def open_scale_window():
    import texture
    texture.open_window()

scale_window_thread = threading.Thread(target=open_scale_window)
scale_window_thread.daemon = True  # 메인 스레드 종료 시 함께 종료되도록 설정
scale_window_thread.start()

# 라인 알림 전송
def send_line_noti(message):
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_NOTI_TOKEN', 'NULL')
    headers = {'Authorization': 'Bearer ' + token}
    data = {"message": message}
    requests.post(api_url, headers=headers, data=data)

try:
    while True:
        output = process.stdout.readline()  # 한 줄씩 읽기
        if output:  # 출력이 있을 경우
            print(output.strip())  # 출력 표시

            # CPU 사용량 추출
            match = re.search(r'(\d+(\.\d+)?)%', output)  # 예: "20.5%"
            if match:
                cpu_usage = float(match.group(1))  # CPU 사용량을 float로 변환
                print(f"현재 CPU 사용량: {cpu_usage}%")

                # CPU 사용량이 s_out 이상인 경우 명령어 실행
                if cpu_usage > s_out:
                    cpu_up_time += check_time  # cpu 초과 사용 시간 증가
                    cpu_down_time = 0  # cpu 이하 시간 초기화
                    print(f"CPU 사용량 {s_out}% 초과, 지속 시간: {cpu_up_time}초")

                    # cpu 사용량 60초 이상: 스케일 아웃
                    if cpu_up_time >= 60:
                        print(f"cpu 사용량 {s_out}% 초과, 스케일 아웃")
                        scale_command = ['docker', 'compose', 'up', '-d', '--scale', f'blog={scale_value}']
                        send_line_noti("스케일 아웃")
                        subprocess.run(scale_command)
                        scale_value += 1   # 스케일 값 증가
                        log_to_csv(cpu_usage, '스케일 아웃')  # 로그 파일에 기록
                        print(scale_command)
                        cpu_up_time = 0   # 시간 초기화
                        scale_check = True

                # CPU 사용량이 s_in 이하인 경우 스케일 다운
                elif cpu_usage < s_in:
                    cpu_down_time += check_time   # 15% 이하 지속 시간 체크
                    cpu_up_time = 0  # 초과 사용 시간 초기화
                    if scale_check:
                        print(f"CPU 사용량 {s_in}% 이하, 지속 시간: {cpu_down_time}초")

                        if cpu_down_time >= 60 and scale_value > 1:
                            print(f"cpu 사용량 {s_in}% 이하, 스케일 인")
                            scale_value -= 1  # 스케일 값 감소
                            scale_command = ['docker', 'compose', 'up', '-d', '--scale', f'blog={scale_value}']
                            send_line_noti("스케일 인")
                            subprocess.run(scale_command)
                            log_to_csv(cpu_usage, '스케일 인')  # 로그 파일에 기록
                            print(scale_command)
                            cpu_down_time = 0  # 시간 초기화

                        # 스케일 값이 1일 때 스케일 다운 중단
                        elif scale_value == 1:
                            scale_check = False

                else:
                    cpu_up_time = 0
                    cpu_down_time = 0

except KeyboardInterrupt:
    print("실행 중지.")
finally:
    process.terminate()  # 프로세스 종료  
