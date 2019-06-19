# Copyright 2018-2019 oscillo
# 
# Permission is hereby granted, free of charge,
# to any person obtaining a copy of this software 
# and associated documentation files (the "Software"),
# to deal in the Software without restriction, 
# including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission 
# notice shall be included in all copies or substantial
# portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
# OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# [[[ 1. Install ]]]
sudo apt-get update
sudo apt-get install -y hostapd dnsmasq unclutter exfat-fuse exfat-utils
sudo aptitude install -y ntfs-3g

# [[[ 2. Config ]]]
# [[ 2.1. wlan0 ]]
if test -e "/home/pi/Desktop/PetitKara/Raspi/wlan0"; then
  sudo cp /home/pi/Desktop/PetitKara/Raspi/wlan0 /etc/network/interfaces.d/wlan0
fi
sudo cp /etc/network/interfaces.d/wlan0 /home/pi/Desktop/PetitKara/Raspi/wlan0
sudo ed /etc/network/interfaces.d/wlan0 << EOF
a
iface lo inet loopback
iface eth0 inet dhcp
allow-hotplug wlan0
iface wlan0 inet static
  address 192.168.9.1
  netmask 255.255.255.0
.
wq
EOF

# [[ 2.2. dhcpcd ]] 
if test -e "/home/pi/Desktop/PetitKara/Raspi/dhcpcd.conf"; then
  sudo cp /home/pi/Desktop/PetitKara/Raspi/dhcpcd.conf /etc/dhcpcd.conf
fi
sudo cp /etc/dhcpcd.conf /home/pi/Desktop/PetitKara/Raspi/dhcpcd.conf
sudo ed /etc/dhcpcd.conf << EOF
$
a
interface wlan0
  static ip_address=192.168.9.1/24
  nohook wpa_supplicant
.
wq
EOF

# [[ 2.3. hostapd ]]
cd /etc/hostapd/
sudo cp /usr/share/doc/hostapd/examples/hostapd.conf.gz .
sudo gzip -d -f hostapd.conf.gz
cpuinfo=$(sum /proc/cpuinfo | cut -d ' ' -f1)
sudo ed /etc/hostapd/hostapd.conf << EOF
%s/ssid=test/ssid=PetitKara$cpuinfo/
wq
EOF

if test -e "/home/pi/Desktop/PetitKara/Raspi/init.d_hostapd"; then
  sudo cp /home/pi/Desktop/PetitKara/Raspi/init.d_hostapd /etc/init.d/hostapd
fi
sudo cp /etc/init.d/hostapd /home/pi/Desktop/PetitKara/Raspi/init.d_hostapd
sudo ed /etc/init.d/hostapd << EOF
%s/DAEMON_CONF=/DAEMON_CONF=\/etc\/hostapd\/hostapd.conf/
wq
EOF

if test -e "/home/pi/Desktop/PetitKara/Raspi/init.d_hostapd"; then
  sudo cp /home/pi/Desktop/PetitKara/Raspi/default_hostapd /etc/default/hostapd
fi
sudo cp /etc/default/hostapd /home/pi/Desktop/PetitKara/Raspi/default_hostapd
sudo ed /etc/default/hostapd << EOF
%s/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/
wq
EOF

# [[ 2.4. ip forward ]]
sudo ed /etc/sysctl.conf << EOF
%s/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/
wq
EOF

# [[ 2.5. iptables ]]
sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -t nat -A  POSTROUTING -o wlan1 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

if test -e "/home/pi/Desktop/PetitKara/Raspi/rc.local"; then
  sudo cp /home/pi/Desktop/PetitKara/Raspi/rc.local /etc/rc.local
fi
sudo cp /etc/rc.local /home/pi/Desktop/PetitKara/Raspi/rc.local
sudo ed /etc/rc.local << EOF
n
i
iptables-restore < /etc/iptables.ipv4.nat
.
wq
EOF

# [[ 2.6. dnsmasq ]]
if test -e "/home/pi/Desktop/PetitKara/Raspi/dnsmasq.conf"; then
  sudo cp /home/pi/Desktop/PetitKara/Raspi/dnsmasq.conf /etc/dnsmasq.conf
fi
sudo cp /etc/dnsmasq.conf /home/pi/Desktop/PetitKara/Raspi/dnsmasq.conf
sudo ed /etc/dnsmasq.conf << EOF
$
a
interface=wlan0
domain-needed
bogus-priv
dhcp-range=192.168.9.50,192.168.9.150,12h
.
wq
EOF

# [[ 2.7. autostart ]]
if test -e "/home/pi/Desktop/PetitKara/Raspi/autostart"; then
  sudo cp /home/pi/Desktop/PetitKara/Raspi/autostart /etc/xdg/lxsession/LXDE-pi/autostart
fi
sudo cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/Desktop/PetitKara/Raspi/autostart
sudo ed /etc/xdg/lxsession/LXDE-pi/autostart << EOF
$
a
@xset s off
@xset -dpms
@xset s noblank
@unclutter
@sh /home/pi/Desktop/PetitKara/start.sh
.
wq
EOF

# [[ 2.8. config.txt ]]
sudo ed /boot/config.txt << EOF
%s/#hdmi_force/hdmi_force/
%s/#hdmi_group/hdmi_group/
%s/#hdmi_mode=1/hdmi_mode=16/
wq
EOF

# [[ 2.9. pcmanfm.conf ]]
sudo ed /etc/xdg/pcmanfm/default/pcmanfm.conf << EOF
%s/autorun=1/autorun=0/
wq
EOF

sudo ed /etc/xdg/pcmanfm/LXDE-pi/pcmanfm.conf << EOF
%s/autorun=1/autorun=0/
wq
EOF

# [[ 2.10. hostapd service ]]

sudo systemctl unmask hostapd
sudo systemctl enable hostapd

# [[[ 3. reboot ]]]

reboot
