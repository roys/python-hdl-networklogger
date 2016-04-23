#!/bin/bash
cd ~/python-hdl-networklogger
/bin/sleep 30	# Just to be more sure that the network interfaces are up and running
/usr/bin/python /home/pi/python-hdl-networklogger/networklogger.py >/home/pi/python-hdl-networklogger/launcher.log 2>&1
