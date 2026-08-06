import os
import sys
import time
import subprocess
import threading
# 欠損エラーが起きるモジュールを明示的に読み込む
import streamlit.runtime.scriptrunner.magic_funcs
import streamlit.web.cli as stcli

def launch_app():
    time.sleep(4)
    # アドレスバーのない専用アプリウィンドウでEdgeを起動
    subprocess.Popen(["cmd", "/c", "start msedge --app=http://localhost:8501"])

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    script_path = os.path.join(base_dir, "子ども会らくらくナビ.py")

    threading.Thread(target=launch_app, daemon=True).start()

    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false",
        "--server.headless=true",
        "--server.port=8501"
    ]
    sys.exit(stcli.main())