## A VScode Tutorial for the ODrive

This guide will help you with using VScode with the ODrive board. 

#### Background.
The ODrive board uses a processor called the STM32F405, which is a member of the ARM Cortex-M4 family. The developers of ODrive have written source code for the STM32, and all of that code can be found here. This documentation is meant to guide you through the process of using VScode in combination with some other tools to connect to the board, and to load firmware. Another section will show you how to use VScode to watch what is happening inside of the STM32 in real time for debugging. 

### Some prerequisites
In order to do this one issue is that you need to set up an coding environment where it is possible to build the ODrive code, and unfortunately, this documentation is not going to cover all the steps required to do this. Here are the prerequisite steps - along with some sources of information - that you will have to perform in order to set up a debugging environment:

* install the odrive development environment described here: [link](https://docs.odriverobotics.com/developer-guide).
* clone a copy of the ODrive code using the command:
```
git clone https://github.com/madcowswe/ODrive.git
```
* follow the instructions [here](https://docs.odriverobotics.com/configuring-vscode.html) to install VScode
* build the .elf file, described [here](https://docs.odriverobotics.com/developer-guide#building-and-flashing-the-firmware)
* flash the ODrive using [stlink](https://docs.odriverobotics.com/odrivetool#flashing-with-an-stlink)

If you were able to do all these things, and it was your first time, congratulations on behalf of the ODrive community, you have earned your entry level developer merit badge. 

### Compiling a build for the ODrive *.elf file for debugging
This section is just for reference. The issue with VScode is you probably can not flash firmware using VScode unless you can also do it on the command line. Let's check that out, start in the /ODrive/Firmware directory
Use the tup.config.default file to create another file named "tup.config".
Make two changes:
1) uncomment the line
  #CONFIG_BOARD_VERSION=v3.5-24V
to work for your board version
2) change the line:
  CONFIG_DEBUG=false
to:
  CONFIG_DEBUG=true
now run:

then check if you have created a new .elf file in the build directory. The file is probably called: build/ODriveFirmware.elf . Also convince yourself that openocd is talking to the stlink device and to your board. Try connecting an stlink to the ODrive board and running:
```openocd -f interface/stlink-v2.cfg -f target/stm32f4x.cfg -c init -c "reset halt" -c "flash write_image erase build/ODriveFirmware.elf" -c "reset run" -c exit```
see [this doc](https://docs.odriverobotics.com/developer-guide#building-and-flashing-the-firmware) for a little bit more information. 

### Flashing a build by running VScode
It is also possible to flash firmware uing VScode. VScode installs on mac, linux and windows. Starting it is a little different for each environment. Once you can get it to run, here is a video to pull a build from github, compile it, flash the firmware, and to save a workspace:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/czsCG6QWvY4/0.jpg)](https://www.youtube.com/watch?v=czsCG6QWvY4)

This is a of summary what is in the video:

* start VScode
* go to Terminal-->New terminal
* get an ODrive buid
```$ git clone https://github.com/madcowswe/ODrive.git```
* go to File-->Add folder to workspace...
* select ODrive/Firmware, hit the "ADD" button. 
* go to File->Save workspace as... and save as a project
* VScode loads all of the project files
* make some changes to tup.config.default in order to do a debugging build
* save as tup.config
* go to Terminal-->New terminal
* use the menu Terminal-->Run Build Task...
* VScode compiles the code
* now make sure your stlink and board are connected
* go to Terminal-->Run task...
* select "Flash"
* boom, VScode flashes the .elf file on to the board

### Debugging using openocd
The openocd project is yet another amazing [open source effort](http://openocd.org/) that enables users to move compiled code on to microprocessors. It works for an incredible number of chips, including the STM32405. It handles that in part by packing a ot of the configuration for flashing the STM32 chip is located in the stlink-v2.cfg and stm32f4f.cfg files. 

But the other thing that openocd can do to do on-chip debugging. This means you can look for bugs or find out what is happening when configuring odrive. You can:
* Start your program, and at the same time connect odrivetool
* Examine variables when you run commands in odrivetool
* Specify just about anything that might impact the behavior of odrive
* Stop and start the program based specified conditions

And by the way, it is absolutely astonishing that any of this is possible. Debuggers are incredible and this, is an amazing world to live in. 

set logging on  
set logging off  
set logging overwrite [on|off] 'cause default is to append  
set logging file FILENAME''


$ ps aux | grep openocd

If things seem to hang be sure to watch your processes and make sure openocd is not running:

http://ardupilot.org/dev/docs/debugging-with-gdb-on-stm32.html

info functions .*Axis
break /Users/owhite/ODrive/Firmware/MotorControl/main.cpp:33
break main

openocd -c gdb_port 50000 -s /Users/owhite/ODrive/Firmware -f interface/stlink-v2.cfg -f target/stm32f4x_stlink.cfg


$ ps aux | grep openocd
