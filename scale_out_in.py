import subprocess
import time
import re

# 모니터링할 컨테이너의 이름 또는 ID
container_name = 'samdul-blog-1'  # 여기에 원하는 컨테이너 이름 또는 ID 입력

# Docker stats 명령어 실행 (특정 컨테이너만 모니터링)
command = ['docker', 'stats', container_name, '--format', 'table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}']

# subprocess.Popen을 사용하여 명령어 실행
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

print(f"{container_name} 컨테이너의 Docker stats 명령어 실행 중...")

scale_value = 2  # 스케일 값 초기화, 1은 이미 있음

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
                
                # CPU 사용량이 50% 이상인 경우 명령어 실행
                if cpu_usage > 50:
                    print("CPU 사용량 50% 초과. 스케일 업")
                    scale_command = ['docker', 'compose', 'up', '-d', '--scale', f'blog={scale_value}']
                    subprocess.run(scale_command)
                    print(scale_command)

                    # 스케일 값 증가
                    scale_value += 1

                    # CPU 사용량이 15% 이하인 경우 스케일 다운
                elif cpu_usage < 15:
                    if scale_value > 1:
                        print("CPU 사용량이 15% 이하입니다. 스케일 다운 명령어 실행 중...")
                        scale_value -= 1  # 스케일 값 감소
                        scale_command = ['docker', 'compose', 'up', '-d', '--scale', f'blog={scale_value}']
                        subprocess.run(scale_command)
                        print(scale_command)
        else:
            break
        # time.sleep(1)  # 1초 대기
except KeyboardInterrupt:
    print("실행 중지.")
finally:
    process.terminate()  # 프로세스 종료

