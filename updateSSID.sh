cp /etc/hostapd/hostapd.conf .

cpuinfo=$(sum /proc/cpuinfo | cut -d ' ' -f1)
sudo ed hostapd.conf << EOF
%s/ssid=.*/ssid=PetitKara$cpuinfo/
wq
EOF

diff /etc/hostapd/hostapd.conf hostapd.conf

if [ $? -ne 0 ]; then
  # unmatch
  sudo cp hostapd.conf /etc/hostapd/
  sudo reboot
fi
