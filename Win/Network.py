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
import socket

class Network:
  # Get wlan0 ip address
  def GetIP(self):
    return socket.gethostbyname(socket.gethostname())
      
  # Get SSID
  def GetSSID(self):
    proc = subprocess.Popen(
      "netsh wlan show interface",
      stdout = subprocess.PIPE, 
      shell = True
    )
    out, err = proc.communicate()
    procLines = out.decode("ascii", "ignore").splitlines()
    for line in procLines:
      if 4 == line.find("SSID"):
        return line[line.find(":")+2:]
    return ""

  # Get Password
  def GetPassword(self):
    proc = subprocess.Popen(
      "chcp 437 & netsh wlan show profiles name=" + self.GetSSID() + " key=clear",
      stdout = subprocess.PIPE,
      shell = True
    )
    out, err = proc.communicate()
    procLines = out.decode("ascii", "ignore").splitlines()
    for line in procLines:
      if 0 < line.find("Key Content"):
        return line[line.find(":")+2:]
    return ""

  # Set Password
  def SetPassword(self, password):
    if None is password:
      subprocess.call("sudo sh /home/pi/Desktop/PetitKara/Raspi/disablePassWD.sh", shell=True)
    else:
      subprocess.call("sudo sh /home/pi/Desktop/PetitKara/Raspi/enablePassWD.sh " + password, shell=True)
