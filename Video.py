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

proc = None       # omxplayer process
stopThread = None # stop thread

# Open and Playing Video
def Open(path,vol) : # None
  global proc
  # [[[ 1. Make playing command ]]]
  command = \
    "omxplayer --no-osd -b -o hdmi --vol " \
    + str(vol) + " \"" \
    + path + "\""
  # [[[ 2. Execute for playing ]]]
  proc = subprocess.Popen( \
    command, \
    shell=True, \
    stdin=subprocess.PIPE)

# Check playing is done
def CheckPlaying() : # Bool True(Playing) / False(Stop)
  global proc
  if proc is not None:
    # < omxplayer is running >
    if proc.poll() is not None:
      # < omxplayer has terminated >
      proc = None
      return False
    else:
      # < omxplayer is running >
      return True
  else:
    # < omxplayer is not running >
    return False

# Set D-Bus Address to Environment Variable
def SetDBusEnvironment() : # None
  # [[[ 1. Open Process Information ]]]
  dbusAddress = open("/tmp/omxplayerdbus.pi","r")
  # [[[ 2. Set Environment Variable ]]]
  os.environ["DBUS_SESSION_BUS_ADDRESS"] = \
    dbusAddress.readline()[0:-1]
  dbusAddress.close()

# Fade Stop Playing Video
def FadeStopThread() : # None
  global proc
  try:
    # < omxplayer is running >
    # [[[ 1. volume down ]]]
    for i in range(15):
      proc.stdin.write(b"-")
      proc.stdin.flush()
      time.sleep(0.2)
    # [[[ 2. exit omxplayer ]]]
    proc.stdin.write(b"q")
    # [[[ 3. Flush stdin ]]]
    proc.stdin.flush()
    # [[[ 4. Terminate omxplayer ]]]
    proc = None
  except:
    pass

# Stop Playing Video
def Stop() : # None
  global stopThread
  # [[[ 1. Create tread that has sleep ]]]
  stopThread = threading.Thread(target=FadeStopThread)
  stopThread.start()

# Pause Video
def Pause() : # None
  global proc
  try:
    # < omxplayer is running >
    # [[[ 1. pause / resume ]]]
    proc.stdin.write(b"p")
    # [[[ 2. Flush stdin ]]]
    proc.stdin.flush()
  except:
    pass

# Switch Audio
def SwitchAudio() : # None
  global proc
  try:
    # < omxplayer is running >
    # [[[ 1. next audio stream ]]]
    proc.stdin.write(b"k")
    # [[[ 2. Flush stdin ]]]
    proc.stdin.flush()
  except:
    pass

# Rewind
def Rewind() : # None
  # [[[ 1. Set D-Bus Address to Environment Variable ]]]
  SetDBusEnvironment()
  # [[[ 2. Call for Seek ]]]
  subprocess.call(b'dbus-send --print-reply=literal --session --dest=org.mpris.MediaPlayer2.omxplayer /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Seek int64:-5000000'.split())

# Fast Forward
def FastForward() : # None
  # [[[ 1. Set D-Bus Address to Environment Variable ]]]
  SetDBusEnvironment()
  # [[[ 2. Call for Seek ]]]
  subprocess.call(b'dbus-send --print-reply=literal --session --dest=org.mpris.MediaPlayer2.omxplayer /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Seek int64:5000000'.split())

# Down Volume
def DownVolume() : # None
  global proc
  try:
    # < omxplayer is running >
    # [[[ 1. next audio stream ]]]
    proc.stdin.write(b"-")
    # [[[ 2. Flush stdin ]]]
    proc.stdin.flush()
  except:
    pass

# Up Volume
def UpVolume() : # None
  global proc
  try:
    # < omxplayer is running >
    # [[[ 1. next audio stream ]]]
    proc.stdin.write(b"+")
    # [[[ 2. Flush stdin ]]]
    proc.stdin.flush()
  except:
    pass
