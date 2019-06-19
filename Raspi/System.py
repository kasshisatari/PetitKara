# -*- coding: utf-8 -*-

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

import time
import os
import subprocess

class System:
  def __init__(self):
    # [[[ 1. Check ALSA Device ]]]
    aplay = subprocess.Popen(
      "aplay -L",
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      env={'LANG':'C'},
      shell=True
    )
    out, err = aplay.communicate()
    aplayLines = out.decode("ascii", "ignore").splitlines()
    alsa = False # True: Exist ALSA Device, False: Not Exist
    for line in aplayLines:
      if -1 != line.find("sndrpijustboomd"): # JustBoom DAC HAT
        alsa = True
        break;
    if True is alsa:
      self.hw = "Raspi:ALSA"
    else:
      self.hw = "Raspi"

  def SetTime(self, time):
    subprocess.call(['sudo', 'date', '--set=' + time ])

  def Shutdown(self):
    os.system("sudo shutdown -h now")

  def Restart(self):
    os.system("sudo shutdown -r now")

  def StartBrowser(self):
    os.system("chromium-browser --noerrdialogs --kiosk --incognito --no-default-browser-check http://localhost:50000/console --no-sandbox --test-type &")

  def GetDir(self):
    # [[[ 1. Wait USB Mass Storage ]]]
    # [[ 1.1. dmesg ]]
    dmesg = subprocess.Popen(
      "dmesg | grep Mass | wc -l",
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      env={'LANG':'C'},
      shell=True
    )
    dmesgOut, dmesgErr = dmesg.communicate()
    dmesgLines = dmesgOut.decode("ascii", "ignore").splitlines()

    # [[ 1.2. /media/pi ]]
    usbMassNum = 0
    for line in dmesgLines:
      usbMassNum = int(line)
    lsNum = 0
    while lsNum != usbMassNum:
      ls = subprocess.Popen(
        "ls /media/pi | wc -l",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={'LANG':'C'},
        shell=True
      )
      lsOut, lsErr = ls.communicate()
      lsLines = lsOut.decode("ascii", "ignore").splitlines()
      for line in lsLines:
        lsNum = int(line)
      time.sleep(0.1)

    # [[[ 2. Return /media/pi ]]]
    return [os.path.sep + 'media' + os.path.sep + 'pi' + os.path.sep]

  def GetHW(self):
    return self.hw

  def UpdatePetitKara(self):
    os.system("cp -fr PetitKara ..")
    os.system("sh install.sh")
