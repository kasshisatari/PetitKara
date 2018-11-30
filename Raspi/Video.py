# -*- coding: utf-8 -*-

# Copyright 2018 oscillo
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
import subprocess
import os
import threading

class Video:
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

    # [[[ 2. Initialize ]]]
    # omxplayer command line
    if False == alsa:
      self.start = "omxplayer --no-osd -b -o hdmi --vol "
    else:
      self.start = "omxplayer --hw --no-osd -b -o alsa:plughw:1,0 --vol "
    self.proc = None       # omxplayer process
    self.stopThread = None # stop thread

  # Open and Playing Video
  def Open(self,path,vol) : # None
    # [[[ 1. Make playing command ]]]
    command = \
      self.start \
      + str(vol) + " \"" \
      + path + "\""
    # [[[ 2. Execute for playing ]]]
    self.proc = subprocess.Popen( \
      command, \
      shell=True, \
      stdin=subprocess.PIPE)

  # Check playing is done
  def CheckPlaying(self) : # Bool True(Playing) / False(Stop)
    if self.proc is not None:
      # < omxplayer is running >
      if self.proc.poll() is not None:
        # < omxplayer has terminated >
        self.proc = None
        return False
      else:
        # < omxplayer is running >
        return True
    else:
      # < omxplayer is not running >
      return False

  # Set D-Bus Address to Environment Variable
  def SetDBusEnvironment(self) : # None
    # [[[ 1. Open Process Information ]]]
    dbusAddress = open("/tmp/omxplayerdbus.pi","r")
    # [[[ 2. Set Environment Variable ]]]
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = \
      dbusAddress.readline()[0:-1]
    dbusAddress.close()

  # Fade Stop Playing Video
  def FadeStopThread(self) : # None
    try:
      # < omxplayer is running >
      # [[[ 1. volume down ]]]
      for i in range(15):
        self.proc.stdin.write(b"-")
        self.proc.stdin.flush()
        time.sleep(0.2)
      # [[[ 2. exit omxplayer ]]]
      self.proc.stdin.write(b"q")
      # [[[ 3. Flush stdin ]]]
      self.proc.stdin.flush()
      # [[[ 4. Terminate omxplayer ]]]
      self.proc = None
    except:
      pass

  # Stop Playing Video
  def Stop(self) : # None
    # [[[ 1. Create tread that has sleep ]]]
    self.stopThread = threading.Thread(target=self.FadeStopThread)
    self.stopThread.start()

  # Pause Video
  def Pause(self) : # None
    try:
      # < omxplayer is running >
      # [[[ 1. pause / resume ]]]
      self.proc.stdin.write(b"p")
      # [[[ 2. Flush stdin ]]]
      self.proc.stdin.flush()
    except:
      pass

  # Switch Audio
  def SwitchAudio(self) : # None
    try:
      # < omxplayer is running >
      # [[[ 1. next audio stream ]]]
      self.proc.stdin.write(b"k")
      # [[[ 2. Flush stdin ]]]
      self.proc.stdin.flush()
    except:
      pass

  # Rewind
  def Rewind(self) : # None
    # [[[ 1. Set D-Bus Address to Environment Variable ]]]
    self.SetDBusEnvironment()
    # [[[ 2. Call for Seek ]]]
    subprocess.call(b'dbus-send --print-reply=literal --session --dest=org.mpris.MediaPlayer2.omxplayer /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Seek int64:-5000000'.split())

  # Fast Forward
  def FastForward(self) : # None
    # [[[ 1. Set D-Bus Address to Environment Variable ]]]
    self.SetDBusEnvironment()
    # [[[ 2. Call for Seek ]]]
    subprocess.call(b'dbus-send --print-reply=literal --session --dest=org.mpris.MediaPlayer2.omxplayer /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Seek int64:5000000'.split())

  # Down Volume
  def DownVolume(self) : # None
    try:
      # < omxplayer is running >
      # [[[ 1. next audio stream ]]]
      self.proc.stdin.write(b"-")
      # [[[ 2. Flush stdin ]]]
      self.proc.stdin.flush()
    except:
      pass

  # Up Volume
  def UpVolume(self) : # None
    try:
      # < omxplayer is running >
      # [[[ 1. next audio stream ]]]
      self.proc.stdin.write(b"+")
      # [[[ 2. Flush stdin ]]]
      self.proc.stdin.flush()
    except:
      pass
