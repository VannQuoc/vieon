from flask import Flask
import multiprocessing
import subprocess
import sys

app = Flask(__name__)

def run_script(script):
    subprocess.run([sys.executable, script])

@app.route('/')
def index():
    return "Hello, World from Flask!"

if __name__ == "__main__":
    # Tạo các quy trình con
    main_process = multiprocessing.Process(target=run_script, args=("main.py",))
    getproxy_process = multiprocessing.Process(target=run_script, args=("getproxy.py",))

    # Bắt đầu các quy trình con
    main_process.start()
    getproxy_process.start()

    # Chạy ứng dụng Flask
    app.run(debug=True, use_reloader=False)

    # Khi ứng dụng Flask dừng lại, các quy trình con cũng nên được dừng lại
    main_process.terminate()
    getproxy_process.terminate()
    main_process.join()
    getproxy_process.join()
