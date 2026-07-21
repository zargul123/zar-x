@echo off
rem Zar X daily ritual ??? run by Windows Task Scheduler (or by hand).
rem Output is appended to journal\daily_runs.log for later reading.
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
echo. >> journal\daily_runs.log
echo ================ %date% %time% ================ >> journal\daily_runs.log
C:\Users\hp\miniconda3\envs\tfdml\python.exe cockpit\brief.py >> journal\daily_runs.log 2>&1
C:\Users\hp\miniconda3\envs\tfdml\python.exe journal\snapshot.py >> journal\daily_runs.log 2>&1
C:\Users\hp\miniconda3\envs\tfdml\python.exe journal\grader.py >> journal\daily_runs.log 2>&1
rem Sync reports to OneDrive so the Commander can read them on mobile
copy /y journal\daily_runs.log "C:\Users\hp\OneDrive\ZarX\daily_runs.log" >nul 2>&1
copy /y journal\snapshots_local.csv "C:\Users\hp\OneDrive\ZarX\snapshots_local.csv" >nul 2>&1
