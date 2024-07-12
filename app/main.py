import subprocess
import uvicorn
import multiprocessing

# 启动 FastAPI 服务器
def start_fastapi_server():
    uvicorn.run("fastapi_server:app", host="0.0.0.0", port=8000, reload=True)

# 启动 GradioUI
def start_gradio_ui():
    subprocess.Popen(["python", "gradio_ui.py"])

if __name__ == "__main__":
    # 使用多进程启动FastAPI服务器和GradioUI
    fastapi_process = multiprocessing.Process(target=start_fastapi_server)
    fastapi_process.start()

    start_gradio_ui()

    # 保持主进程运行
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("终止应用程序")
        fastapi_process.terminate()