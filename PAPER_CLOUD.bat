@echo off
rem Zar X - the Paper-Watch, THE CLOUD's RECORD. PAPER ONLY. NO MONEY.
rem Fetches the latest from GitHub and opens the cloud's report in Notepad.
rem It changes nothing on this computer: it only reads what the cloud wrote.
rem Needs the internet.
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
git fetch -q origin
git show origin/main:journal/paper_cloud_report.txt > "%TEMP%\zarx_paper_cloud.txt"
start notepad "%TEMP%\zarx_paper_cloud.txt"
