@echo off
rem Zar X - the Paper-Watch. PAPER ONLY. NO MONEY. No order is ever sent.
rem Fetches the latest prices, writes down any new signal, and opens the
rem report in Notepad. Safe to run as often as you like: a second run the
rem same day writes nothing new.
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
C:\Users\hp\miniconda3\envs\tfdml\python.exe journal\paper_watch.py > "%TEMP%\zarx_paper.txt"
start notepad "%TEMP%\zarx_paper.txt"
