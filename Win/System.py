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
import threading

class System:
  def SetTime(self, time):
    pass

  def Shutdown(self):
    os.system("shutdown -s -f")

  def Restart(self):
    os.system("shutdown -r -f")

  def StartBrowser(self):
    os.system("start microsoft-edge:http://localhost:50000/console")
    threading.Thread(target=self.MaximizeBrowser).start()

  def MaximizeBrowser(self):
    time.sleep(3)
    os.system("cscript //nologo Win\\fullscreen.js")

  def GetDir(self):
    drives = []
    for drive in "defghijklmnopqrstuvwxyz":
      if True is os.path.exists(drive + ":" + os.path.sep):
        drives.append(drive + ":" + os.path.sep)
    return drives

  def GetHW(self):
    return "Win"

  def UpdatePetitKara(self):
    os.system("xcopy PetitKara . /e /y")
    os.system("install.bat")
