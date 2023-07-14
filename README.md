# OAT FirmWare GUI
OpenAstroTech FirmWare Graphical User Interface -- A graphical way to build and load firmware onto an OpenAstroTracker/OpenAstroMount.

## Supported platforms
- Windows 64 bit
- Linux 64 bit
  - Requires Python 3.7+, libc >= 2.28 (check with `ldd --version`)

MacOS _might_ work, don't have a mac to test on. Drop a line if you're willing to test it!

## Installing
Simply download the [latest release](https://github.com/OpenAstroTech/OATFWGUI/releases), unzip and run:
- Windows: `OATFWGUI_Windows.bat`
- Linux: `OATFWGUI_Linux.sh`
  - Override the python interpreter by setting `PYTHON` (i.e. `PYTHON=/usr/bin/python3.10 ./OATFWGUI_Linux.sh`)
  - This creates a local python virtual environment in `.venv_OATFWGUI`. If there's an error during the first run, delete that folder to have the script try again.

> :warning: **OATFWGUI requires an active internet connection!**

## Uninstalling
OATFWGUI only has two directories:
1. Find the plaformio core directory and delete it
    * Open up a log file from the `logs` folder
    * Near the top will be a log line like `DEBUG:Setting PLATFORMIO_CORE_DIR to C:\Users\RUNNER~1\AppData\Local\Temp\.pio_OATFWGUI_dev-0.0.9-c3592b`
    * This step is not necessary on Linux, the folder is automatically removed when the computer is restarted
2. Delete the extracted folder (something like `OATFWGUI_1.0.0-release+f5e4f6_Windows_X64`)

## Screenshots
Windows:
![](assets/screenshot_Windows.jpg)

Linux:
![](assets/screenshot_Linux.jpg)
