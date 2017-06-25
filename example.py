#! /usr/bin/env nix-shell
#! nix-shell -i python -p python27Packages.pyserial python27Packages.netifaces
from qnapdisplay import QnapDisplay
from datetime import timedelta

import time
import platform
import netifaces as ni

Lcd = QnapDisplay()

if Lcd.Init:
    while True:
        Lcd.Write(0, platform.node())
        Lcd.Write(1, platform.system() + " " + platform.release())

        time.sleep(3)

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds = uptime_seconds))

        Lcd.Write(0, "uptime")
        Lcd.Write(1, uptime_string);

        time.sleep(3)

        list_of_interfaces = [ 'enp5s0', 'enp6s0', 'enp9s0', 'enp10s0' ]
        for interface in list_of_interfaces:
            Lcd.Write(0, interface)
            try:
                ni.ifaddresses(interface)
                ip = ni.ifaddresses(interface)[2][0]['addr']
                Lcd.Write(1, ip);
            except:
                Lcd.Write(1, "no ip address");

            time.sleep(3)

else:
    print 'Oops something went wrong here'
