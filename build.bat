:set dist path
set version_path=..\target\AutoSpeechTest

:ready env
python -m pip install --upgrade pip
pip install -r ./requirements.txt

cd python

:delete software, runtime data and execute result but not delete config
rd /s /q %version_path%\AutoSpeechTest
rd /s /q %version_path%\output
rd /s /q %version_path%\temp

:build software
pyinstaller -D AutoSpeechTest.py --distpath=%version_path%

:copy config and replace old config
xcopy ..\res\application.yml ..\target\AutoSpeechTest\res\ /E/Y
xcopy ..\res\sox-14-4-2 ..\target\AutoSpeechTest\AutoSpeechTest\ /E/Y

:set work path to project root
rd /s /q .\build
del /f /s /q *.spec
cd ..