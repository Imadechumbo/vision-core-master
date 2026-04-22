@echo off
setlocal
set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%organize_vision_core_extracted.py" "%~1"
endlocal
