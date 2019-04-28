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
import threading
import ctypes
from Win import vlc

class Video:
  def __init__(self):
    # [[[ 1. Initialize ]]]
    # vlc command line
    self.instance = vlc.Instance()
    self.player = self.instance.media_player_new()
    self.stopThread = None # stop thread
    self.vol = self.GetDefaultVolume()

  # Open and Playing Video
  def Open(self,path,vol,audioNum, audioIndex) : # None
    # [[[ 1. Make playing command ]]]
    self.player.release()
    self.player = self.instance.media_player_new()
    self.player.set_fullscreen(True)
    self.player.audio_set_volume(int(vol / 100))
    self.player.set_mrl(path, "audio-track=" + str(audioIndex - 1))
    self.player.play()

    # [[[ 2. Initialize Audio Stream Switching ]]]
    self.audioNum = audioNum
    self.audioStream = audioIndex
    self.vol = vol

    # [[[ 3. Monitor Video Window ]]]
    self.playing = threading.Thread(target=self.Playing)
    self.playing.start()

  # Always On Top
  def Playing(self): # None
    # [[[ 1. Foreground Video Window ]]]
    while 0 == ctypes.windll.user32.FindWindowW(None, "VLC (Direct3D Output)") \
      and 0 == ctypes.windll.user32.FindWindowW(None, "VLC (Direct3D11 output)"):
      time.sleep(0.1)
    hwnd = ctypes.windll.user32.FindWindowW(None, "VLC (Direct3D Output)")
    if 0 == hwnd:
      hwnd = ctypes.windll.user32.FindWindowW(None, "VLC (Direct3D11 output)")
    ctypes.windll.user32.SetWindowPos(hwnd,-1,0,0,0,0,2|1)

    # [[[ 2. Monitor Video End ]]]
    while -1 == self.player.get_media().get_duration():
      time.sleep(0.1)
    while self.player.get_time() < self.player.get_media().get_duration():
      time.sleep(0.5)

    # [[[ 3. Terminate Playing Video ]]]
    self.player.stop()

  # Check playing is done
  def CheckPlaying(self) : # Bool True(Playing) / False(Stop)
    status = self.player.get_state()
    if status == vlc.State.NothingSpecial or status == vlc.State.Stopped:
      # < vlc is stop >
      return False
    else:
      # < vlc is running >
      return True

  # Fade Stop Playing Video
  def FadeStopThread(self) : # None
    try:
      # < vlc is running >
      # [[[ 1. volume down ]]]
      for i in range(15):
        self.DownVolume()
        time.sleep(0.2)
      # [[[ 2. exit vlc ]]]
      self.player.stop()
    except:
      pass

  # Stop Playing Video
  def Stop(self) : # None
    # [[[ 1. Create tread that has sleep ]]]
    self.stopThread = threading.Thread(target=self.FadeStopThread)
    self.stopThread.start()

  # Pause Video
  def Pause(self) : # None
    self.player.pause()

  # Switch Audio
  def SwitchAudio(self) : # None
    # [[[ 1. Check audio number ]]]
    if 1 == self.audioNum:
      return

    # [[[ 2. Change audio stream ]]]
    self.audioStream = self.audioStream + 1
    if self.audioNum < self.audioStream:
      # [[ 2.1. back audio stream ]]
      self.audioStream = 1
    self.player.audio_set_track(self.audioStream)

  # Position
  def Position(self) : # [sec]
    return int(self.player.get_time()/1000)

  # Rewind
  def Rewind(self) : # None
    pos = self.player.get_time() - 1000 * 5;
    if pos < 0:
      pos = 0
    self.player.set_time(pos)

  # Fast Forward
  def FastForward(self) : # None
    pos = self.player.get_time() + 1000 * 5;
    if self.player.get_media().get_duration() < pos:
      self.player.stop()
    else:
      self.player.set_time(pos)

  # Down Volume
  def DownVolume(self) : # None
    self.vol = self.vol - 300
    self.player.audio_set_volume(int(self.vol / 100))

  # Up Volume
  def UpVolume(self) : # None
    self.vol = self.vol + 300
    self.player.audio_set_volume(int(self.vol / 100))

  # Default Volume
  def GetDefaultVolume(self): # Integer [dB]
    return 4500
