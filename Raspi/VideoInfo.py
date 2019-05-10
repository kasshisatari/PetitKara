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
import re
import os

class VideoInfo:
  def __init__(self):
    self.file = None

  # Update Information
  def UpdateInfo(self):
    # [[[ 1. Call omxplayer -i ]]]
    ifconfig = subprocess.Popen(
      "omxplayer -i \"" + self.file + "\"",
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      env={'LANG':'C'},
      shell=True
    )
    out, err = ifconfig.communicate()
    ifconfigLines = err.decode("ascii", "ignore").splitlines()

    # [[[ 2. Parse omxplayer -i output ]]]
    self.duration = ""
    self.audioNum = 0
    self.audioName = []
    self.videoEncode = ""
    self.resolution = ""
    audioIndex = 1
    for line in ifconfigLines:
      # [[ 2.1. Get Duration: ]]
      if "Duration:" in line:
        blocks = line.split()
        self.duration = blocks[1][0:-1]
      if "Stream" in line and "Audio:" in line:
        self.audioNum = self.audioNum + 1
      if "Stream" in line and "Video:" in line:
        blocks = line.split()
        self.videoEncode = blocks[3]
        self.resolution = \
          re.sub("\[[^\]]*\]","",\
            re.sub("\([^\)]*\)","",line)).split(",")[2].split()[0]
      if "handler_name" in line and self.audioNum > 0:
        self.audioName.append(str(audioIndex) + ":" + line[line.index(" : ") + 3:])
        audioIndex = audioIndex + 1
    if [] == self.audioName:
      for audioIndex in range(self.audioNum):
        self.audioName.append(str(audioIndex) + ":" )

  # Get Resolution
  def GetResolution(self, file):
    # [[[ 1. Check Filename ]]]
    if file == self.file:
      return self.resolution

    # [[[ 2. Update Information ]]]
    self.file = file
    self.UpdateInfo()
    return self.resolution

  # Get VideoEncode
  def GetVideoEncode(self, file):
    # [[[ 1. Check Filename ]]]
    if file == self.file:
      return self.videoEncode

    # [[[ 2. Update Information ]]]
    self.file = file
    self.UpdateInfo()
    return self.videoEncode

  # Get Duration
  def GetDuration(self, file):
    # [[[ 1. Check Filename ]]]
    if file == self.file:
      return self.duration

    # [[[ 2. Update Information ]]]
    self.file = file
    self.UpdateInfo()
    return self.duration

  # Get Number of Audio Stream
  def GetAudioNum(self, file):
    # [[[ 1. Check Filename ]]]
    if file == self.file:
      return self.audioNum

    # [[[ 2. Update Information ]]]
    self.file = file
    self.UpdateInfo()
    return self.audioNum

  # Get Name of Audio Stream
  def GetAudioName(self, file):
    # [[[ 1. Check Filename ]]]
    if file == self.file:
      return self.audioName

    # [[[ 2. Update Information ]]]
    self.file = file
    self.UpdateInfo()
    return self.audioName

  # Get Tag of Audio Stream
  def GetAudioTag(self, file):
    # [[[ 1. Check Filename ]]]
    audioName = []
    if file == self.file:
      for audioIndex in range(1, self.audioNum + 1):
        audioName.append(\
          "<option value=\"" + str(audioIndex) + "\">" +  \
          self.audioName[audioIndex - 1] + \
          "</option>")
      return audioName

    # [[[ 2. Update Information ]]]
    self.file = file
    self.UpdateInfo()
    for audioIndex in range(1, self.audioNum + 1):
      audioName.append(\
        "<option value=\"" + str(audioIndex) + "\">" +  \
        self.audioName[audioIndex - 1] + \
        "</option>")
    return audioName
