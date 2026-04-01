@echo off
cd %~dp0
call venv\Scripts\activate
start http://127.0.0.1:5000
python sistema-tapecaria/app.py
pause
