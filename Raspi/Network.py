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

import subprocess

class Network:
  # Get wlan0 ip address
  def GetIP(self):
    # [[[ 1. Call ifconfig ]]]
    ifconfig = subprocess.Popen(
      "ifconfig",
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      env={'LANG':'C'},
      shell=True
    )
    out, err = ifconfig.communicate()
    ifconfigLines = out.decode("ascii", "ignore").splitlines()

    # [[[ 2. Parse ifconfig output ]]]
    wlan = 0 # wlan0 block
    for line in ifconfigLines:
      # [[ 2.1. Check wlan0 block ]]
      if line.startswith("wlan0"):
        wlan = 1
        continue
      # [[ 2.2. Get wlan0 ip address ]]
      if "inet " in line and 1 == wlan:
        blocks = line.split()
        return blocks[1]

  # Get USB Wifi (wlan1)
  def GetUSBWifi(self):
    iwconfig = subprocess.Popen(
      "iwconfig",
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      env={'LANG':'C'},
      shell=True
    )
    out, err = iwconfig.communicate()
    iwconfigLines = out.decode("ascii", "ignore").splitlines()
    wifi = False
    for line in iwconfigLines:
      if 0 == line.find("wlan1"):
        wifi = True
    return wifi

  # Get USB Wifi SSID
  def GetUSBWifiSSID(self):
    ssid = None
    wpa_supplicant = open("/etc/wpa_supplicant/wpa_supplicant.conf")
    for line in wpa_supplicant:
      if 0 <= line.find("ssid="):
        ssid = line[line.find("ssid=")+6:-2]
    wpa_supplicant.close()
    return ssid

  # Get USB Wifi Password
  def GetUSBWifiPassWD(self):
    passwd = None
    wpa_supplicant = open("/etc/wpa_supplicant/wpa_supplicant.conf")
    for line in wpa_supplicant:
      if 0 <= line.find("#psk="):
        passwd = line[line.find("#psk=")+6:-2]
    wpa_supplicant.close()
    return passwd

  # Get USB Wifi Config
  def GetUSBWifiConfig(self):
    wpa_supplicant = open("/etc/wpa_supplicant/wpa_supplicant.conf")
    for line in wpa_supplicant:
      if 0 == line.find("network="):
        return True
    return False

  # Get SSID
  def GetSSID(self):
    hostapd = open("/etc/hostapd/hostapd.conf")
    for line in hostapd:
      if 0 == line.find("ssid="):
        ssid = line[5:-1]
    hostapd.close()
    return ssid

  # Get Password
  def GetPassword(self):
    hostapd = open("/etc/hostapd/hostapd.conf")
    valid = False
    password = None
    for line in hostapd:
      if 0 == line.find("wpa=2"):
        valid = True
      elif 0 == line.find("wpa_passphrase="):
        password = line[15:-1]
    hostapd.close()
    if False == valid:
      password = ""
    return password

  # Set Password
  def SetPassword(self, password):
    if None is password:
      subprocess.call("sudo sh /home/pi/Desktop/PetitKara/Raspi/disablePassWD.sh", shell=True)
    else:
      subprocess.call("sudo sh /home/pi/Desktop/PetitKara/Raspi/enablePassWD.sh " + password, shell=True)

  # Set USB Wifi
  def SetUSBWifi(self, ssid, password):
    if True is self.GetUSBWifiConfig():
      subprocess.call("sh /home/pi/Desktop/PetitKara/Raspi/deleteNetwork.sh", shell=True)
    if len(ssid) > 0 and len(password) > 7:
      subprocess.call("sh /home/pi/Desktop/PetitKara/Raspi/addNetwork.sh " + ssid + " " + password, shell=True)
