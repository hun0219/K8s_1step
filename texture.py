import tkinter as tk
import subprocess
#import sys
#import os

#sys.path.append(os.path.dirname(__file__))
#from scale_out_in import log_to_csv
#import scale_out_in

# 초기 스케일 값 설정
scale_value = 1

# 스케일 인 함수
def scale_in():
    global scale_value
    if scale_value > 1:  # 스케일 값이 1보다 클 때만 감소
        scale_value -= 1
        print(f"스케일 인: blog={scale_value}")
        scale_command = ['docker', 'compose', 'up', '-d', '--scale', f'blog={scale_value}']
        subprocess.run(scale_command)
        #log_to_csv(cpu_usage, '스케일 인')

# 스케일 아웃 함수
def scale_out():
    global scale_value
    scale_value += 1
    print(f"스케일 아웃: blog={scale_value}")
    scale_command = ['docker', 'compose', 'up', '-d', '--scale', f'blog={scale_value}']
    subprocess.run(scale_command)
    #log_to_csv(cpu_usage, '스케일 아웃')

# 메인 윈도우 생성
root = tk.Tk()
root.title("수동 스케일 인/아웃")
root.geometry("300x200")

# 버튼 생성
button1 = tk.Button(root, text="스케일 인", command=scale_in)
button2 = tk.Button(root, text="스케일 아웃", command=scale_out)
button1.pack(pady=40)  # 버튼을 윈도우에 추가하고 패딩 적용
button2.pack(pady=10)  # 버튼을 윈도우에 추가하고 패딩 적용

# 메인 루프 실행
root.mainloop()

