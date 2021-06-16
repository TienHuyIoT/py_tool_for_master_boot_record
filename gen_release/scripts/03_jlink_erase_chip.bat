@echo off
echo Erase
set file="C:\04 Project\01. Xoontec\01_WatchMe\ProductionToolsWatchMe\gen_release\scripts\jlink_scripts\erase.jlink"
cd /d "C:\Program Files (x86)\SEGGER\JLink"
JLink.exe -device NRF52840_XXAA -CommandFile %file%