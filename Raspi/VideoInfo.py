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

import subprocess

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
    for line in ifconfigLines:
      # [[ 2.1. Get Duration: ]]
      if "Duration:" in line:
        blocks = line.split()
        self.duration = blocks[1][0:-1]
      if "Stream" in line and "Audio:" in line:
        self.audioNum = self.audioNum + 1

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
