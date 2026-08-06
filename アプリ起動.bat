@echo off
chcp 65001 > nul
cd /d "C:\Users\300004\Desktop\前崎\その他\自治会_こども会関係\アプリ"

echo 裏で動いている古いシステムを強制終了しています...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo Microsoft Edgeでシステムを起動します...
start msedge http://localhost:8501

python -m streamlit run "子ども会らくらくナビ.py" --server.headless true
pause