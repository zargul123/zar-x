@echo off
rem ==========================================================================
rem Zar X - THE OPEN-INTEREST RECORDER, run monthly by Windows Task Scheduler.
rem
rem WHY THIS ONE MATTERS MORE THAN THE OTHER ALARMS: Binance keeps only 30 days
rem of open-interest history and refuses anything older. Whatever falls off the
rem back of that window is gone permanently and cannot be bought back later at
rem any price. Every other source this ship uses serves deep history on demand.
rem This one does not.
rem
rem WHY MONTHLY IS ENOUGH: every run reaches back the full 30 days, so a single
rem missed month loses nothing. TWO missed months in a row would. That is why
rem the task is set to StartWhenAvailable - if the laptop was off on the 1st,
rem Windows runs it as soon as the laptop is next on.
rem
rem IT MUST RUN HERE, NOT IN THE CLOUD. GitHub's runners are US-hosted and
rem Binance geo-blocks US addresses, so a cloud recorder might collect nothing,
rem silently, for weeks - on the one dataset that cannot be recovered.
rem
rem Written 2026-07-27 on the Commander's instruction.
rem ==========================================================================
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1

echo. >> journal\daily_runs.log
echo ======== open-interest recorder %date% %time% ======== >> journal\daily_runs.log

C:\Users\hp\miniconda3\envs\tfdml\python.exe data\open_interest.py --record >> journal\daily_runs.log 2>&1
set RC=%ERRORLEVEL%

if not "%RC%"=="0" (
  echo RECORDER FAILED - exit code %RC%. NOTHING WAS WRITTEN. >> journal\daily_runs.log
  echo The 30-day window is still rolling. Run it by hand or tell a session. >> journal\daily_runs.log
  goto :sync
)

rem Preserve the rows off this laptop. The whole point of the recorder is that
rem this data cannot be re-fetched later, so a copy that exists only here is
rem one disk failure away from being no copy at all. Scoped to the history
rem folder ONLY - it can never sweep up a session's work in progress.
rem Every git command below is restricted to data/oi_history with an explicit
rem pathspec. A bare "git commit" would sweep up whatever a session happened to
rem leave staged, and an unattended task must never commit work it did not do.
git add data/oi_history >> journal\daily_runs.log 2>&1
git diff --cached --quiet -- data/oi_history
if errorlevel 1 (
  git commit -m "oi: monthly open-interest rows recorded by the laptop task" -- data/oi_history >> journal\daily_runs.log 2>&1
  git push >> journal\daily_runs.log 2>&1
) else (
  echo No new rows to commit - already up to date. >> journal\daily_runs.log
)

:sync
rem Second off-laptop copy, same as the other alarms do for the journal.
if not exist "C:\Users\hp\OneDrive\ZarX\oi_history" mkdir "C:\Users\hp\OneDrive\ZarX\oi_history" >nul 2>&1
copy /y data\oi_history\*.csv "C:\Users\hp\OneDrive\ZarX\oi_history\" >nul 2>&1
copy /y journal\daily_runs.log "C:\Users\hp\OneDrive\ZarX\daily_runs.log" >nul 2>&1
