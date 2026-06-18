@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "REPO_PATH=%~dp0"
if "%REPO_PATH:~-1%"=="\" set "REPO_PATH=%REPO_PATH:~0,-1%"

echo ============================================================
echo TW Quant Cockpit v1.2.8 Post-release One-click Verification
echo Repo: %REPO_PATH%
echo ============================================================
echo.

if not exist "%REPO_PATH%\main.py" (
    echo [FAIL] main.py not found under:
    echo %REPO_PATH%
    exit /b 2
)

set "FAILED=0"

set "LABEL=Version Info"
call :run python "%REPO_PATH%\main.py" version-info

set "LABEL=Replay Health"
call :run python "%REPO_PATH%\main.py" replay-health

set "LABEL=Replay Scenario Health"
call :run python "%REPO_PATH%\main.py" replay-scenario-health

set "LABEL=Replay Session Manager Health"
call :run python "%REPO_PATH%\main.py" replay-session-manager-health

set "LABEL=Replay Journal Health"
call :run python "%REPO_PATH%\main.py" replay-journal-health

set "LABEL=Replay Scoring Health"
call :run python "%REPO_PATH%\main.py" replay-scoring-health

set "LABEL=Replay Strategy Health"
call :run python "%REPO_PATH%\main.py" replay-strategy-health

set "LABEL=Replay Timeframe Health"
call :run python "%REPO_PATH%\main.py" replay-timeframe-health

set "LABEL=Replay Review Health"
call :run python "%REPO_PATH%\main.py" replay-review-health

set "LABEL=Replay Challenge Health"
call :run python "%REPO_PATH%\main.py" replay-challenge-health

set "LABEL=Replay Registry Health"
call :run python "%REPO_PATH%\main.py" replay-registry-health

set "LABEL=Intelligence Stable"
call :run python "%REPO_PATH%\main.py" intelligence-stable

set "LABEL=Intelligence Stable Checks"
call :run python "%REPO_PATH%\main.py" intelligence-stable-checks

set "LABEL=Safety Scan Docs"
call :run python "%REPO_PATH%\main.py" safety-scan --target docs

set "LABEL=Safety Scan All"
call :run python "%REPO_PATH%\main.py" safety-scan --target all

set "LABEL=Research Cockpit Stable"
call :run python "%REPO_PATH%\main.py" research-cockpit-stable --mode real

set "LABEL=Research Cockpit Stable Checks"
call :run python "%REPO_PATH%\main.py" research-cockpit-stable-checks

set "LABEL=Stable v0.6.0 Check"
call :run python "%REPO_PATH%\main.py" stable-v060-check --mode real

set "LABEL=Release Gate Regression"
call :run python "%REPO_PATH%\main.py" regression-run --suite release_gate --mode real

set "LABEL=Quick Regression"
call :run python "%REPO_PATH%\main.py" regression-run --suite quick --mode real

set "LABEL=Mock Realtime Smoke"
call :run python "%REPO_PATH%\main.py" mock-realtime --duration 10

set "LABEL=Paper Smoke"
call :run python "%REPO_PATH%\main.py" paper

set "LABEL=Git Status"
call :run git -C "%REPO_PATH%" status

set "LABEL=Git Short Status"
call :run git -C "%REPO_PATH%" status -sb

set "LABEL=Git HEAD"
call :run git -C "%REPO_PATH%" rev-parse HEAD

set "LABEL=Git origin/main"
call :run git -C "%REPO_PATH%" rev-parse origin/main

set "LABEL=Git v1.2.8 Tag"
call :run git -C "%REPO_PATH%" tag -l v1.2.8

echo.
echo ============================================================
if "%FAILED%"=="0" (
    echo [PASS] All one-click verification commands completed.
    echo Review WARN or expected BLOCKED entries in the output.
    set "EXIT_CODE=0"
) else (
    echo [FAIL] One or more commands returned a non-zero exit code.
    echo Failed command count: %FAILED%
    set "EXIT_CODE=1"
)
echo ============================================================
echo.
pause
exit /b %EXIT_CODE%

:run
echo.
echo ------------------------------------------------------------
echo [RUN] %LABEL%
echo ------------------------------------------------------------
%*
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
    echo [FAIL] %LABEL% returned exit code %RC%
    set /a FAILED+=1
) else (
    echo [PASS] %LABEL%
)
exit /b 0
