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

Information on the sense hat: https://www.raspberrypi.org/blog/the-sense-hat-headgear-for-the-terminally-curious/

Installation
------------

Clone this repository on your Raspberry Pi.

Run the barometer with
```bash
sudo python3 barometerRun.py
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
