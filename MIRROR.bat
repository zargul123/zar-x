@echo off
rem Zar X - the Mirror. Your logged trades, what the instruments had
rem recorded, and the same trades sized to risk 1 percent.
rem Arithmetic only. It READS your journal and never writes to it.
rem The report opens in Notepad.
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
C:\Users\hp\miniconda3\envs\tfdml\python.exe journal\mirror.py > "%TEMP%\zarx_mirror.txt"
start notepad "%TEMP%\zarx_mirror.txt"
