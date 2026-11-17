@echo off
rem Zar X - the Paper-Watch, THE LAPTOP's RECORD. PAPER ONLY. NO MONEY.
rem No order is ever sent. Fetches the latest prices, writes down any new
rem signal in the laptop's own record, and opens the report in Notepad.
rem Safe to run as often as you like: a second run the same day writes
rem nothing new. It first picks up the cloud's record from GitHub, so the
rem report can say whether the two records agree (skipped if offline).
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
git fetch -q origin >nul 2>&1
git merge -q --ff-only origin/main >nul 2>&1
C:\Users\hp\miniconda3\envs\tfdml\python.exe journal\paper_watch.py > "%TEMP%\zarx_paper.txt"
start notepad "%TEMP%\zarx_paper.txt"
