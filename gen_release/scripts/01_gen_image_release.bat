@echo off

echo ============================================================
echo ===============Script generate release image================
echo ============================================================

set script_path="C:\04 Project\01. Xoontec\01_WatchMe\ProductionToolsWatchMe\gen_release\scripts"

set boot_image_hex=..\boot\boot_app.hex
set boot_image_bin=..\boot\boot_app.bin

set mainApp_hex=..\app\main_app.hex
set mainApp_bin=..\app\main_app.bin
set mainHeader_hex=..\app\mainHeader.hex
set mbr_hex=..\mbr\mbr.hex
set mbr_main_release=..\final\mbr_main_release.hex

set mbr_mainHeader_hex=..\mbr\mbr_appHeader.hex

::rem Save current directory
set curdir=%cd%
echo %cd%

::run script build_mainHeader.bat the first to gen main_app.bin
echo [release] run script build_mainHeader.bat
call ..\app\build_mainHeader.bat

::rem Restore current directory
cd %curdir%
echo %cd%

::Generating main application dfu encrypt image from main_app.bin file
echo [release] main application dfu encrypt image
python ..\..\build_dfu_encrypt_firmware.py

::Mergehex: using j-flash tool
echo Mergehex "mbr_hex" and "mainHeader_hex" %mbr_hex%
mergehex --merge %mbr_hex% %mainHeader_hex% --output %mbr_mainHeader_hex%

echo Generating image file %mbr_main_release%
mergehex --merge %mainApp_hex% %mbr_mainHeader_hex% --output %mbr_main_release%

::Delete hex file template
del %mbr_mainHeader_hex%

IF ERRORLEVEL 1 goto ERROR
goto END
:ERROR
ECHO J-Flash saveas hex file: Error!
pause
:END