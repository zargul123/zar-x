@echo off
rem Zar X - the Paper-Watch, THE WEEK'S NUMBERS for the weekly autopsy.
rem PAPER ONLY. NO MONEY. Reads what is already recorded; fetches nothing.
rem Numbers only: the reading of them is done in a session.
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
C:\Users\hp\miniconda3\envs\tfdml\python.exe journal\paper_watch.py --week > "%TEMP%\zarx_paper_week.txt"
start notepad "%TEMP%\zarx_paper_week.txt"
