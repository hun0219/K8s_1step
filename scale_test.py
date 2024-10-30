import subprocess

print("Docker stats 명령어 실행 중...")

try:
    command = [
        'docker', 
        'stats', 
        '--no-stream',  # 단 한번만 데이터 수집
        '--format', 
        'table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}'
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    print("명령어 실행 완료.")

    if result.returncode == 0:
        print("출력:\n", result.stdout)
    else:
        print("오류:\n", result.stderr)

except Exception as e:
    print("예외 발생:", e)

