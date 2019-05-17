# Encoders

## Known and Supported Encoders
Be sure to read the [ODrive Encoder Guide](https://docs.google.com/spreadsheets/d/1OBDwYrBb5zUPZLrhL98ezZbg94tUsZcdTuwiVNgVqpU).

## Encoder Calibration
Please take into account that all encoder types supported by ODrive require that you do some sort of encoder calibration. This requires the following:
* selecting an encoder and mounting it to your motor
* choosing an interface (e.g., AB, ABI or SPI)
* connecting the pins to the odrive
* loading the correct odrive firmware (the default will work in many cases)
* motor calibration
* saving the settings in the odrive for correct bootup

## Startup sequence notes

The following are variables that MUST be set up for your encoder configuration. Your values will vary depending on your encoder:

* odrv0.axis0.encoder.config.cpr = 4000
* odrv0.axis0.encoder.config.mode = ENCODER_MODE_INCREMENTAL

The following are examples of values that MAY impact the success of calibration. Your values will vary depending on your setup:
* odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
* odrv0.axis0.encoder.config.cpr = 4000
* odrv0.axis0.encoder.config.calib_range = 0.05
* odrv0.axis0.motor.config.calibration_current = 10.0
* odrv0.axis0.motor.config.resistance_calib_max_voltage = 12.0
* odrv0.axis0.controller.config.vel_limit = 50000

Lots of other values can get you. It's a process. Thankfully there is a lot of good people that will help you debug calibration problems. 

If calibration works, congratulations.

Now try: 
* odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
* odrv0.axis0.controller.set_vel_setpoint(3000,0) 
let it loop a few times and then set:
* odrv0.axis0.requested_state = AXIS_STATE_IDLE

Do you still have no errors? Awesome. Now set these variables:
* odrv0.axis0.encoder.config.pre_calibrated = True
* odrv0.axis0.motor.config.pre_calibrated  = True 

And see if ODrive agrees that calibration worked by just running
* odrv0.axis0.encoder.config.pre_calibrated

(using no "= True" ). Make sure that variable is in fact True. 

Also, if you have calibrated and encoder.pre_calibrated is equal to true, and you had no errors so far. Run this: 
* odrv0.axis0.encoder.config.use_index = True
* odrv0.save_configuration()
* odrv0.reboot()

and see if you can do after a bootup you can run: 
* odrv0.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH

and get no errors. 

## Encoder Problems

There are several issues that may prevent you from completing encoder calibration. 

ODrive may not complete the calibrate sequence when you go to:
* odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

It completes the calibrate sequence after:
* odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

but fails after you go to:
* odrvN.axisN.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

Or maybe it vibrates in an entertaining way. See:
https://www.youtube.com/watch?v=gaRUmwvSyAs

## Encoder Signals

If your encoder is properly connected, run the command:
* odrv0.axis0.encoder.shadow_count 

and look at your value. Then turn your motor by hand and see if that value changes. Also, notice that the command:
* odrv0.axis0.encoder.config.cpr = 4000

must reflect the number of counts odrive receives after one complete turn of the motor. So use shadow_count to test if that is working properly. 

You will probably never be able to properly debug if you have problems unless you use an oscilloscope. If you have one, try the following:
Connect to the AB pins, see if you get square waves as you turn the motor.
Connect to the I pin, see if you get a pulse on a complete rotation. Sometimes this is hard to see.
If you are using SPI, connect to CLK, and CS pins, look for a signal like this:
[INSERT PIC]

## Encoder Signals
Noise is found in all circuits, life is just about figuring out if it is preventing your system from working. Lots of users have no problems with noise interferring with their odrive operation, others will tell you "_I've been using the same encoder as you with no problems_". Power to 'em, that may be true, but it doesn't mean it will work for you. If you are concerned about noise, there are several things that might cause noise in your system:

* encoder wires are too close to motor wires
* long wires
* ribbon cable

The following _might_ mitigate noise problems. Use twisted pairs, where one side of each twisted pair is tied to ground, the other side is tied to your signal. If you are using SPI, use a 20-50 ohm resistor in series on CLK, which is more susceptable noise.

## AS5047/AS5048 Encoders
The AS5047/AS5048 encoders are Hall Effect/Magenetic sensors that can serve as rotary encoders for the ODrive.

The AS5047 has 3 independent output interfaces: SPI, ABI, and PWM. 
The AS5048 has 4 independent output interfaces: SPI, ABI, I2C, and PWM.

Both chips come with evaluation boards that can simplify mounted the chips to your motor. For our purposes if you are using an evaluation board you should select the settings for 3.2v, and tie MOSI high to 3.2v. 

If you are having calibration problems - make sure your magnet is centered on the axis of rotation on the motor, some users report this has a significant impact on calibration. Also make sure your magnet height is within range of the spec sheet. 

Using ABI. 
You can use ABI with the AS5047/AS5048 with the default ODrive firmware. For your wiring, connect A, B, 3.2v, GND to the labeled pins on the odrive
The acronym I and Z mean the same thing, connect those as well if you are using an index signal. 

Using SPI.

TobinHall has written a [branch](https://github.com/TobinHall/ODrive/tree/Non-Blocking_Absolute_SPI) that supports the SPI option on the AS5047/AS5048. Use his build to flash firmware on your ODrive and connect MISO, SCK, and CS to the labeled pins on the odrive

Tie MOSI to 3.2v, connect to the SCK, CLK, MISO, GND and 3.2v pins on the ODrive. (note for SPI users, the acronym SCK and CLK mean the same thing, the acronym CSn and CS mean the same thing.)

