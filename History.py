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

from datetime import datetime
import os
import threading

fileName = "hisotry.db" # DB File Name
conn = None             # SQLite Connection
c = None                # SQLite Cursor
lock = threading.Lock() # Lock Object

# Initialize DB
def init(): # None
  global conn
  global c
  # [[[ 1. Initialize DB ]]]
  # [[ 1.1. Prepare SQLite ]]
  import sqlite3
  conn = sqlite3.connect(fileName, check_same_thread=False)
  c = conn.cursor()
  # [[ 1.2. Check Table ]]
  c.execute("select * from sqlite_master " +
    "where type='table' and name='History'")
  if c.fetchone() is None:
    # < No Table >
    # [ 1.2.1. Create History Table ]
    c.execute("CREATE TABLE [History] " + 
      "(" +
      "[Path] TEXT NOT NULL, " +
      "[User] TEXT, " +
      "[Comment] TEXT, " +
      "[Time] TEXT);")

# Add
def Add(
      path,    # String(In): File Full Path
      user,    # String(In): User Name 
      comment  # String(In): Comment
    ): # Bool True(Success) / False(Failure)
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("begin")

  # [[[ 2. Insert Last Record ]]]
  c.execute("insert into History values("+
    "\"" + path + "\"," +
    "\"" + user + "\"," +
    "\"" + comment + "\"," +
    "\"" + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "\")")

  # [[[ 3. UnLock ]]]
  conn.commit()
  lock.release()

  return True

# List Records
def List(): # list(tuple(Path,User,Comment,Time))
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("begin")

  # [[[ 2. Initialize List ]]]
  list = []

  # [[[ 3. Make List ]]]
  for row in c.execute("select * from History order by Time desc"):
    list.append((row[0],row[1],row[2],row[3]))

  # [[[ 4. UnLock ]]]
  conn.rollback()
  lock.release()
  return list

# Get Historylist Tags
def Historylist():
  list = ''
  for row in List():
    list = list + \
      "<li style=\"white-space:pre-line;\">" + \
      row[1] + "<br>" + \
      os.path.basename(row[0]) + "<br>" + \
      row[2] + \
      "</li>"
  return list

# Delete History
def Delete():
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()

  # [[[ 2. Close ]]]
  if conn is not None:
    conn.close()

  # [[[ 3. Delete DB ]]]
  if os.path.exists("./" + fileName):
    os.remove(fileName)

  # [[[ 4. Initialize DB]]]
  init()

  # [[[ 5. Unlock ]]]
  lock.release()
  return

init()
