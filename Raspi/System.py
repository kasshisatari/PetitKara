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
  def SetTime(self, time):
    subprocess.call(['sudo', 'date', '--set=' + time ])

  def Shutdown(self):
    os.system("sudo shutdown -h now")

  def Restart(self):
    os.system("sudo shutdown -r now")

  def StartBrowser(self):
    os.system("chromium-browser --noerrdialogs --kiosk --incognito --no-default-browser-check http://localhost:50000/console &")

  def GetDir(self):
    return [os.path.sep + 'media' + os.path.sep + 'pi' + os.path.sep]

  def GetHW(self):
    return self.hw
