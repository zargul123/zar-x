@echo off
rem ==========================================================================
rem Zar X - THE OPEN-INTEREST RECORDER, run WEEKLY by Windows Task Scheduler.
rem
rem WHY THIS ONE MATTERS MORE THAN THE OTHER ALARMS: Binance keeps only 30 days
rem of open-interest history and refuses anything older. Whatever falls off the
rem back of that window is gone permanently and cannot be bought back later at
rem any price. Every other source this ship uses serves deep history on demand.
rem This one does not.
rem
rem IT MUST RUN HERE, NOT IN THE CLOUD. GitHub's runners are US-hosted and
rem Binance geo-blocks US addresses, so a cloud recorder might collect nothing,
rem silently, for weeks - on the one dataset that cannot be recovered.
rem
rem Written 2026-07-27 on the Commander's instruction.
rem
rem --- REPAIRED 2026-08-03, GATE 3.2c-R1, after R-037 -----------------------
rem
rem WAS MONTHLY. IT IS NOW WEEKLY, AND THAT IS THE BIGGEST PART OF THE REPAIR.
rem The old comment here said "every run reaches back the full 30 days, so a
rem single missed month loses nothing. TWO missed months in a row would."
rem THAT REASONING WAS WRONG AND 2026-08-03 IS WHERE IT BROKE. The task did not
rem MISS - it RAN, silently did nothing, and reported success, and the next
rem attempt was a month away. ONE silent failure was enough to put 99
rem irreplaceable rows one month from deletion. On a weekly cadence a silent
rem failure costs nothing at all, because the next run still reaches back a
rem full 30 days.
rem
rem TWO: THIS JOB NO LONGER SHARES A LOG FILE. Six jobs were released in the
rem same second on 2026-08-03 and five of them wrote NOTHING - not even their
rem header - because only one process can append to a file at a time, and the
rem losers simply gave up. The recorder was one of the five. It now writes to
rem journal\oi_recorder.log, which nothing else touches.
rem
rem THREE: THE ALARM IS NO LONGER ADDRESSED TO A FILE THAT MAY BE UNAVAILABLE,
rem and this batch now ends by reporting THE RECORDER'S exit code rather than
rem the copy's. The old version ended on `copy`, so Windows recorded 0 - and
rem CHECK_STATUS.bat printed that 0 to the Commander as "OK".
rem
rem FOUR, AND THE ONE THAT CATCHES A CAUSE NOBODY HAS PROVED: CHECK_STATUS.bat
rem no longer asks Windows how this job went. It asks data\collection_guard.py
rem how old the newest row in the archive is. The job can lie. The data cannot.
rem ==========================================================================
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
set LOG=journal\oi_recorder.log

echo. >> %LOG%
echo ======== open-interest recorder %date% %time% ======== >> %LOG%

C:\Users\hp\miniconda3\envs\tfdml\python.exe data\open_interest.py --record >> %LOG% 2>&1
set RC=%ERRORLEVEL%

if not "%RC%"=="0" (
  echo RECORDER FAILED - exit code %RC%. NOTHING WAS WRITTEN. >> %LOG%
  echo The 30-day window is still rolling. Run it by hand or tell a session. >> %LOG%
  goto :sync
)

rem Preserve the rows off this laptop. The whole point of the recorder is that
rem this data cannot be re-fetched later, so a copy that exists only here is
rem one disk failure away from being no copy at all. Scoped to the history
rem folder ONLY - it can never sweep up a session's work in progress.
rem Every git command below is restricted to data/oi_history with an explicit
rem pathspec. A bare "git commit" would sweep up whatever a session happened to
rem leave staged, and an unattended task must never commit work it did not do.
git add data/oi_history >> %LOG% 2>&1
git diff --cached --quiet -- data/oi_history
if errorlevel 1 (
  git commit -m "oi: weekly open-interest rows recorded by the laptop task" -- data/oi_history >> %LOG% 2>&1
  git push >> %LOG% 2>&1
) else (
  echo No new rows to commit - already up to date. >> %LOG%
)

:sync
rem Second off-laptop copy, same as the other alarms do for the journal.
if not exist "C:\Users\hp\OneDrive\ZarX\oi_history" mkdir "C:\Users\hp\OneDrive\ZarX\oi_history" >nul 2>&1
copy /y data\oi_history\*.csv "C:\Users\hp\OneDrive\ZarX\oi_history\" >nul 2>&1
copy /y %LOG% "C:\Users\hp\OneDrive\ZarX\oi_recorder.log" >nul 2>&1

rem TELL WINDOWS THE TRUTH. The copies above must never decide what Task
rem Scheduler records, because "Last Result: 0" is what CHECK_STATUS.bat used
rem to print as OK over a job that collected nothing.
exit /b %RC%
