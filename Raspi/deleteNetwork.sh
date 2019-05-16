sudo ed /etc/wpa_supplicant/wpa_supplicant.conf << EOF
/network=/
.,\$d
wq
EOF


