#!/bin/bash

sudo cp /etc/network/interfaces.host /etc/network/interfaces

sudo ifdown wlan0
sudo ifup wlan0

sudo service dnsmasq start
sudo service hostapd start
