@echo off
rem Zar X - log a trade you have CLOSED. Seven questions, plain words.
rem Nothing here judges the trade: that is the Mirror's job, monthly.
rem Nothing is written until all seven are answered.
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
C:\Users\hp\miniconda3\envs\tfdml\python.exe journal\log_trade.py
echo.
pause
