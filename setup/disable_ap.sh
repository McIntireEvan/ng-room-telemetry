#!/bin/bash

sudo service hostapd stop
sudo service dnsmasq stop

sudo cp /etc/network/interfaces.client /etc/network/interfaces

sudo ifdown wlan0
sudo ifup wlan0
