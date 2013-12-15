garagedoor
==========

Raspi Garage Door opener.

This is alpha - use totally at your own risk. 

Install: 

Set up opendoor to run on boot

python opendoor.py 8081 
(Or whatever port you want)

link bin/opendoor to your executable path somewhere. 

add an admin user - script it in /database. Edit first with a passcode.

Packages needed on the Raspi:

gpio
webpy

