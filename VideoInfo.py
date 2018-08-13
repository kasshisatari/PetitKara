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

# Get Duration
def GetDuration(file):
  # [[[ 1. Call omxplayer -i ]]]
  ifconfig = subprocess.Popen(
    "omxplayer -i \"" + file + "\"",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env={'LANG':'C'},
    shell=True
  )
  out, err = ifconfig.communicate()
  ifconfigLines = err.decode("ascii", "ignore").splitlines()

  # [[[ 2. Parse omxplayer -i output ]]]
  for line in ifconfigLines:
    # [[ 2.1. Get Duration: ]]
    if "Duration:" in line:
      blocks = line.split()
      return blocks[1][0:-1]
