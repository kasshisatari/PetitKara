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
import subprocess
import os
import threading
import dbus

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
      self.start = "omxplayer --no-osd -b -o alsa:plughw:1,0 --vol "
    self.proc = None       # omxplayer process
    self.stopThread = None # stop thread

  # Open and Playing Video
  def Open(self,path,vol,audioNum, audioIndex) : # None
    # [[[ 1. Make playing command ]]]
    command = \
      self.start \
      + str(vol) \
      + " -n " + str(audioIndex) + " \"" \
      + path + "\""
    # [[[ 2. Execute for playing ]]]
    self.proc = subprocess.Popen( \
      command, \
      shell=True, \
      stdin=subprocess.PIPE)
    # [[[ 3. Initialize Audio Stream Switching ]]]
    self.audioNum = audioNum
    self.audioStream = 0
    self.vol = vol

    # [[[ 4. D-Bus ]]]
    flag = True
    while True == flag:
      try:
        while False == os.path.exists("/tmp/omxplayerdbus.pi"):
          time.sleep(0.05)
        time.sleep(0.05)
        dbusAddress = open("/tmp/omxplayerdbus.pi", "r")
        self.bus = dbus.bus.BusConnection(dbusAddress.readline()[0:-1])
        dbusAddress.close()
        self.proxy = self.bus.get_object(
          'org.mpris.MediaPlayer2.omxplayer',
          '/org/mpris/MediaPlayer2',
          introspect=False)
        self.root_interface = dbus.Interface(
          self.proxy,
          'org.mpris.MediaPlayer2')
        self.player_interface = dbus.Interface(
          self.proxy,
          'org.mpris.MediaPlayer2.Player')
        self.properties_interface = dbus.Interface(
          self.proxy,
          'org.freedesktop.DBus.Properties')
        flag = False
      except:
        pass

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

  # Fade Stop Playing Video
  def FadeStopThread(self) : # None
    try:
      # < omxplayer is running >
      # [[[ 1. volume down ]]]
      for i in range(15):
        self.DownVolume()
        time.sleep(0.2)
      # [[[ 2. exit omxplayer ]]]
      self.root_interface.Quit()
      # [[[ 3. Terminate omxplayer ]]]
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
      self.player_interface.PlayPause()
    except:
      pass

  # Switch Audio
  def SwitchAudio(self) : # None
    # [[[ 1. Check audio number ]]]
    if 1 == self.audioNum:
      return

    # [[[ 2. Change audio stream ]]]
    self.audioStream = self.audioStream + 1
    if self.audioNum == self.audioStream:
      # [[ 2.1. back audio stream ]]
      self.audioStream = 0
    try:
      self.player_interface.SelectAudio(self.audioStream)

      # [[[ 3. Seek for change audio immediately ]]]
      self.player_interface.Seek(dbus.types.Int64(1))
    except:
      pass

  # Position
  def Position(self) : # [sec]
    return self.properties_interface.Get(
      self.player_interface.dbus_interface,
      "Position"
    ) / 1000000

  # Rewind
  def Rewind(self) : # None
    try:
      self.player_interface.Seek(dbus.types.Int64(1000*1000*(-5)))
    except:
      pass

  # Fast Forward
  def FastForward(self) : # None
    try:
      self.player_interface.Seek(dbus.types.Int64(1000*1000*(5)))
    except:
      pass

  # Down Volume
  def DownVolume(self) : # None
    self.vol = self.vol - 300
    try:
      self.properties_interface.Set(
        self.player_interface.dbus_interface,
        "Volume",
        pow(10,self.vol/2000.0)
      )
    except:
      pass

  # Up Volume
  def UpVolume(self) : # None
    self.vol = self.vol + 300
    try:
      self.properties_interface.Set(
        self.player_interface.dbus_interface,
        "Volume",
        pow(10,self.vol/2000.0)
      )
    except:
      pass
