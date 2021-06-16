@ECHO off

set mainApp_path="C:\04 Project\01. Xoontec\01_WatchMe\ProductionToolsWatchMe\gen_release\app"
set jlink_path="C:\Program Files (x86)\SEGGER\JLink"

::rem Save current directory
set curdir=%cd%
echo %cd%

::Using for convert mainHeader application bin2hex
::Set path bin file input
set mainHeader_bin=%mainApp_path%\mainHeader.bin
::Set path hex file output
set mainHeader_hex=%mainApp_path%\mainHeader.hex
set mainHeader_start_addr=0x15FE0
set mainHeader_stop_addr=0x15FF0

::Using for convert main application hex2bin
::Set path hex file input
set mainApp_hex=%mainApp_path%\main_app.hex
::Set path bin file output
set mainApp_bin=%mainApp_path%\main_app.bin
set mainApp_start_addr=0x61000
set mainApp_stop_addr=0x100000

::Set path Jlink
cd /d %jlink_path%
ECHO convert main_app.hex to main_app.bin
ECHO JFlash open a hex file, saveas bin file and exit
ECHO bin file from %mainApp_start_addr% to %mainApp_stop_addr%
JFlash.exe -open%mainApp_hex% -saveas%mainApp_bin%,%mainApp_start_addr%,%mainApp_stop_addr% -exit
TIMEOUT /T 1

::rem Restore current directory
cd %curdir%
echo %cd%
ECHO generate mainHeader.bin
python ..\..\build_mainHeader.py

::Set path Jlink
cd /d %jlink_path%

ECHO convert mainHeader.bin to mainHeader.hex
ECHO JFlash open a bin file, saveas hex file and exit
ECHO bin file from %mainHeader_start_addr% to %mainHeader_stop_addr%
JFlash.exe -open%mainHeader_bin%,%mainHeader_start_addr% -saveas%mainHeader_hex%,%mainHeader_start_addr%,%mainHeader_stop_addr% -exit

::Delete bin file template
del %mainHeader_bin%

::rem Restore current directory
cd %curdir%
echo %cd%

IF ERRORLEVEL 1 goto ERROR
goto END
:ERROR
ECHO J-Flash saveas hex file: Error!
pause
:END