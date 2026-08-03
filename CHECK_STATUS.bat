@echo off
title Zar X - Status Check
rem --- CHANGED 2026-08-03, GATE 3.2c-R1, after R-037 -------------------------
rem This screen used to read Windows' LastTaskResult and print "OK" when it was
rem 0. On 2026-08-03 the open-interest recorder collected nothing and Windows
rem recorded 0, so THIS SCREEN WOULD HAVE CONFIRMED THE FAILURE AS A SUCCESS.
rem The exit code is still shown - it is a fact - but it is now labelled as
rem Windows' opinion, and the archive block below asks THE DATA instead.
rem ---------------------------------------------------------------------------
cd /d "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
powershell -NoProfile -Command "Write-Host '===== ZAR X STATUS =====' -ForegroundColor Cyan; Write-Host ''; Write-Host '--- Laptop alarms: what WINDOWS believes (not evidence - see below) ---' -ForegroundColor Yellow; foreach ($n in @('ZarX Morning Brief','ZarX Snapshot 0105','ZarX Snapshot 0505','ZarX Snapshot 1305','ZarX Snapshot 1705','ZarX Evening Snapshot','ZarX Open Interest')) { $i = Get-ScheduledTaskInfo -TaskName $n; $ok = if ($i.LastTaskResult -eq 0) {'exit 0'} elseif ($i.LastRunTime.Year -lt 2020) {'never yet'} else {('code ' + $i.LastTaskResult)}; Write-Host ('  ' + $n.PadRight(24) + ' ' + $i.LastRunTime.ToString('dd-MMM HH:mm') + '  ' + $ok) }; Write-Host '  (a job that does nothing can still report exit 0 - that is R-037)' -ForegroundColor DarkGray"
echo.
C:\Users\hp\miniconda3\envs\tfdml\python.exe data\collection_guard.py
echo.
powershell -NoProfile -Command "Write-Host '--- Newest black-box rows (times are UTC = PKT minus 5) ---' -ForegroundColor Yellow; Get-Content 'C:\Users\hp\Downloads\zargul trader\zar-x\journal\snapshots_local.csv' -Tail 6 | ForEach-Object { Write-Host ('  ' + $_) }; Write-Host ''; Write-Host 'Cloud guard: check github.com/zargul123/zar-x - latest commit should be a recent cloud snapshot.' -ForegroundColor Green"
pause
