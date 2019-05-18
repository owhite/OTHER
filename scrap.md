## The ODrive Homing and Endpoint Branch

The default ODrive firmware relies on your encoder to find a reference position, by issuing the command:

* `<odrv>.<axis>.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH`

In this scenario the motor will spin until the Z pin changes state. That's fine to tell you the rotational position of the motor. But what happens when your motor has to rotate multiple times before your board is aware that it is in the right position? 

For example, many robotics and CNC activities require a procedure known as _homing_. In these situations it is useful to allow your motor to move until a physical or electronic device orders the system to stop. That _endstop_ can be used as a reference point, and once the ODrive has hit that position it may then want to move to a final home position.

This version of ODrive firmware enables users to use the ODrive gpio pins to connect to phyiscal limit switches, or other sensors that will serve as endpoint detectors. 

### Getting started

Before you plunge into using this endpoint firmware, you will have to perform the following steps. 

* Checkout the ODrive-Endpooint firmware
* Compile and load the firmware
* Configure your ODrive to calibrate a motor
* Perform encoder offset calibration
* Save the configuration and reboot

Describing how to complete above steps is outside of the scope of this documentation. Refer to [this site](https://github.com/madcowswe/ODrive) for more information, and don't hesitate to visit the [odrive forum](https://discourse.odriverobotics.com/) or [odrive discord chat site](https://discourse.odriverobotics.com/t/come-chat-with-us/281). There is a lot of good information at those resources. 

### Configuring the ODrive to perform homing. 

First, you will  need to be able to wire some devices to the ODrive digital inputs. To get you started this is a diagram of switches and devices that could work to detect your endpoints. 

![Endpoint figure](/endpoint_figure.png)

You will have to work out the details of connecting your device. There are a lot of options. Once you have loaded the ODrive-Endpoint firmware and attached some endpoint switches to the gpio pins, power up your ODrive. Perform your motor and encoder calibration, save your settings, and reboot.

Test the device connections to the ODrive board by activating the device, and then in odrive tool type:

* `something something something`

to look at the status of your endpoint gpio pin. 

If you are ready to start testing homing procedures, these variables will then need to be set:
* `<odrv>.<axis>.config.max_endstop.gpio_num = <1, 2, 3, 4, 5, 6, 7, 8>` pick one
* `<odrv>.<axis>.config.min_endstop.gpio_num = <1, 2, 3, 4, 5, 6, 7, 8>` pick one
* `<odrv>.<axis>.config.max_endstop.enabled = <True, False>` probably want True

`gpio_num` refers to the pin used to detect a change in your switch
`enabled` should be self explanatory

For a more final configuration, the following are variables might eventually be set:
* `<odrv>.<axis>.config.max_endstop.offset = <int>` 
* `<odrv>.<axis>.config.max_endstop.is_active_high = <True, False>` 
* `<odrv>.<axis>.min_endstop.config.debounce_ms = <Float>` 
* `<odrv>.<axis>.max_endstop.config.debounce_ms = <Float>` 

`offset` works aas a home switch position. It applies to min_endstop and represents the number of counts required to get home. Suppose home is 100 counts away from min_endstop, set this value to -100. 

`is_active_high` sets the polarity of the endstop. When the switch is pressed it pulls the pin LOW (this is very common for endstop switches), you want to set this to “False”.

`debounce_ms` is a good practice for digital inputs, read up on it [here](https://en.wikipedia.org/wiki/Switch). 'debounce_ms' units are in miliseconds. 

After setting up your configuration, always make sure things are getting stored by running:
* `<odrv>.save_configuration()`
and then reboot. 
