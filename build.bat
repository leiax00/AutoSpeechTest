:set dist path
set version_path=..\target\AutoSpeechTest

:ready env
python -m pip install --upgrade pip
pip install -r ./requirements.txt

cd python

:delete software, runtime data and execute result but not delete config
set software_p=%version_path%\ast_app
set output_p=%version_path%\output
set temp_p=%version_path%\temp
if exist %software_p% (
    rd /s /q %software_p%
)
if exist %output_p% (
    rd /s /q %output_p%
)
if exist %temp_p% (
    rd /s /q %temp_p%
)

:build software
pyinstaller -D ast_app.py --distpath=%version_path%

:copy config and replace old config
copy ..\res\application.yml ..\target\AutoSpeechTest\res\ /Y
xcopy ..\res\sox-14-4-2 ..\target\AutoSpeechTest\ast_app\ /E/Y

:set work path to project root
rd /s /q .\build
del /f /s /q *.spec
cd ..