Visual Barometer for the Raspberry Pi Sense Hat
===============================================

Overview
--------

Uses the onboard pressure meter on the sense hat and the 8x8 RGB LED Matrix to visualize the atmospheric changes.
The pressure is mapped to the colors red (low pressure) to blue (high pressure).

The pressure is measured 10x second and averaged over 4 minutes. Then the averaged pressure is mapped to a color and
displayed on the LED matrix. The previously displayed pressure values are shifted one position. This way the pressure
variations are displayed over time.

The barometer starts by using the current pressure and a small interval around it to map pressure to the red to blue
color interval. As time goes it picks up the maximum and minimum pressure and readjusts. This way you will see
interesting patterns immediately but the converge to a range representative of your environment.

Values can be logged to a CSV file and the initial HIGH/LOW range can be set through the command line.


Information on the sense hat: https://www.raspberrypi.org/blog/the-sense-hat-headgear-for-the-terminally-curious/

Installation
------------

Clone this repository on your Raspberry Pi. I'm running the Debian Jessie distribution with python3.4

Run the barometer with
```bash
python3 barometerRun.py --help
```
to see the configuration options.
```
usage: barometerRun.py [-h] [--initiallow INITIALLOW]
                       [--initialhigh INITIALHIGH] [--updaterate UPDATERATE]
                       [--log LOGFILENAME]

Visualize ambient pressure variations by color coding the pressure on the RPi
Sense Hat

optional arguments:
  -h, --help            show this help message and exit
  --initiallow INITIALLOW
                        Pressure mapped to red color until a lower pressure is
                        observed
  --initialhigh INITIALHIGH
                        Pressure mapped to blue color until a higher pressure
                        is observed
  --updaterate UPDATERATE
                        Update rate in seconds
  --log LOGFILENAME     Name of CSV file for logging pressure

```

If you want to leave it running without having an open terminal consider using tmux or screen

Development
-----------

Unit tests for the code are in `test.py`. Run them with
```bash
python3 test.py
```

License
-------

This software is written by Hrafnkell Eiríksson <he@klaki.net>, @hrafnkelle on Twitter.

It is made available under the GPL v2, see the LICENSE.txt file in this repository.

Copyright (C) 2015 Hrafnkell Eiríksson
