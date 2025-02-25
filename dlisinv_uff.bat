REM setting basis for operation
set BASEPATH=C:\Users\mario\Documents\venvs
set ENVNAME=dlisinv
set ENVPATH=%BASEPATH%\%ENVNAME%

REM Set the working directory where the script will run
cd /d C:\Users\mario\Documents\GitHub\dlis_investigation

REM Activate Conda base environment in the Command Prompt
if exist "%ENVPATH%" rmdir /s /q "%ENVPATH%"

REM Remove and recreate the environment
REM call C:\Users\mario\AppData\Local\Programs\Python\Python38-32\python -m venv %ENVPATH%
call C:\Users\mario\AppData\Local\Programs\Python\Python312\python.exe -m venv %ENVPATH%

REM Activate the newly created environment
call "%ENVPATH%\Scripts\activate.bat"

REM Install your library
call pip install -e.

REM Install the dlispy library
call pip install C:\Users\mario\Documents\GitHub\dlispy

REM Install another libraries
call pip install scipy
call pip install matplotlib
call pip install pandas

pause