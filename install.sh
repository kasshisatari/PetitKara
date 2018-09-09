sudo apt-get update
sudo apt-get install -y hostapd dnsmasq unclutter
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

sudo ed /etc/dhcpcd.conf << EOF
$
a
interface wlan0
static ip=address=192.168.9.1/24
.
wq
EOF

cd /etc/hostapd/
sudo cp /usr/share/doc/hostapd/examples/hostapd.conf.gz .
sudo gzip -d -f hostapd.conf.gz
sudo ed /etc/hostapd/hostapd.conf << EOF
%s/ssid=test/ssid=PetitKara/
wq
EOF

sudo ed /etc/init.d/hostapd << EOF
%s/DAEMON_CONF=/DAEMON_CONF=\/etc\/hostapd\/hostapd.conf/
wq
EOF

sudo ed /etc/default/hostapd << EOF
%s/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/
wq
EOF

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

sudo ed /home/pi/.config/lxsession/LXDE-pi/autostart << EOF
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

sudo ed /boot/config.txt << EOF
%s/#hdmi_force/hdmi_force/
%s/#hdmi_group/hdmi_group/
%s/#hdmi_mode=1/hdmi_mode=16/
.
wq
EOF

reboot
