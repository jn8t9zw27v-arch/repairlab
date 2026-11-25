@echo off
setlocal
cd /d "%~dp0"
echo Publishing RepairLab to the repository you supplied.
echo You may be asked to sign in to GitHub by Git Credential Manager.
echo Do not paste passwords or tokens into the chat.
where git >nul 2>nul
if errorlevel 1 (
  set "GIT_EXE=C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1119-907-0_26.1119.907.0_x64__3k8sg7r9htsxt\dependencies\native\git\cmd\git.exe"
) else (
  set "GIT_EXE=git"
)
"%GIT_EXE%" push -u origin main --tags
if errorlevel 1 (
  echo Upload did not complete. Keep this error message for troubleshooting.
  pause
  exit /b 1
)
echo Upload completed. Verify files at https://github.com/jn8t9zw27v-arch/repairlab
pause
