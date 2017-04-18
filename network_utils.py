import subprocess
import re

interface = "wlp5s0"

def get_networks():
    # Get all the local networks through a bash command
    p1 = subprocess.Popen(["sudo", "iwlist", interface,"scan"], stdout=subprocess.PIPE)
    p2 = subprocess.check_output(["grep", "ESSID"], stdin=p1.stdout)
    raw_names = p2.split('\n')

    # Strip out everything but the network name
    for i in xrange(0, len(raw_names)):
        val = raw_names[i]
        raw_names[i] = re.findall(r'\"(.+)\"', val)

    # Remove dupes
    networks = []
    for id in raw_names:
        if len(id) > 0:
            if id[0] not in networks:
                networks.append(id[0])
    return networks

def generate_wpa_supplicant_wpa2(ssid, identity, password):
    wpa = open("configs/wpa_supplicant.conf", 'w+')
    wpa.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
    wpa.write("update_config=1\n")
    wpa.write("country=US\n\n")

    p1 = subprocess.Popen(["echo", "-n", password], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["iconv", "-t", "utf16le"], stdin=p1.stdout, stdout=subprocess.PIPE)
    hashedpass = subprocess.check_output(["openssl", "md4"], stdin=p2.stdout)
    hashedpass = hashedpass.split('=')[1][1:]

    network_config = "network={{\n ssid=\"{}\" \n key_mgmt=WPA-EAP \n eap=PEAP \n identity=\"{}\" \n password=hash:{} \n phase2=\"auth=MSCHAPV2\"\n}}\n"
    network_config = network_config.format(ssid, identity, hashedpass)

    wpa.write(network_config)