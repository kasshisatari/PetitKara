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

import threading
import os
import re
fileName = "book.db"    # DB File Name
maxRecord = 30          # Max Book Record
BookId = None           # BookId
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
    "where type='table' and name='Book'")
  if c.fetchone() is None:
    # < No Table >
    # [ 1.2.1. Create Book Table ]
    c.execute("CREATE TABLE [Book] " + 
      "([BookId] INTEGER NOT NULL DEFAULT '0' UNIQUE, " +
      "[Idx] INTEGER NOT NULL DEFAULT '1' UNIQUE, " +
      "[Path] TEXT NOT NULL, " +
      "[User] TEXT, " +
      "[Comment] TEXT, " +
      "[Visible] BOOLEAN DEFAULT '1', " +
      "[Duration] TEXT, " +
      "[Dummy] BOOLEAN DEFAULT '0', " +
      "PRIMARY KEY(BookId));")

# Add Top Record
def AddTop(
      path,    # String(In): File Full Path
      user,    # String(In): User Name 
      comment, # String(In): Comment
      visible, # Bool  (In): True(Visible) / False(UnVisible)
      duration,# String(In): Duration
      dummy    # Bool  (In): Dummy
    ): # Bool True(Success) / False(Failure)
  global conn
  global c
  global BookId
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("begin")

  # [[[ 2. Calc BookId ]]]
  if BookId is None:
    # < BookId is valid >
    # [[ 2.1. Get PrevBookId ]]
    c.execute("select max(BookId) from Book")
    prevBookId = c.fetchone()[0]
    if prevBookId is None:
      # < Record is None >
      BookId = -1
    else:
      # < Record is Exist >
      BookId = int(prevBookId)
  # [[ 2.2. CountUp BookId ]]
  BookId = BookId + 1

  # [[[ 3. Calc Idx ]]]
  # [[ 3.1. Get LastIdx ]]
  c.execute("select max(Idx) from Book")
  lastIdx = c.fetchone()[0]
  if lastIdx == maxRecord:
    conn.rollback()
    lock.release()
    return False

  # [[[ 4. Update Idx ]]]
  idx = lastIdx
  if not lastIdx is None:
    while idx > 0:
      c.execute("update Book " +
        "set Idx = " + str(idx+1) + " " +
        "where Idx = " + str(idx))
      idx = idx - 1

  # [[[ 5. Insert Last Record ]]]
  c.execute("insert into Book values("+
    str(BookId) + "," +
    str(1) + "," +
    "\"" + path + "\"," +
    "\"" + user + "\"," +
    "\"" + comment + "\"," +
    str(int(visible)) + "," +
    "\"" + duration + "\"," +
    str(int(dummy)) + ")")

  # [[[ 6. UnLock ]]]
  conn.commit()
  lock.release()

  return True



# Add Last Record
def AddLast(
      path,    # String(In): File Full Path
      user,    # String(In): User Name 
      comment, # String(In): Comment
      visible, # Bool  (In): True(Visible) / False(UnVisible)
      duration,# String(In): Duration
      dummy    # Bool  (In): Dummy
    ): # Bool True(Success) / False(Failure)
  global conn
  global c
  global BookId
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("begin")

  # [[[ 2. Calc BookId ]]]
  if BookId is None:
    # < BookId is valid >
    # [[ 2.1. Get PrevBookId ]]
    c.execute("select max(BookId) from Book")
    prevBookId = c.fetchone()[0]
    if prevBookId is None:
      # < Record is None >
      BookId = -1
    else:
      # < Record is Exist >
      BookId = int(prevBookId)
  # [[ 2.2. CountUp BookId ]]
  BookId = BookId + 1

  # [[[ 3. Calc Idx ]]]
  # [[ 3.1. Get LastIdx ]]
  c.execute("select max(Idx) from Book")
  lastIdx = c.fetchone()[0]
  if lastIdx is None:
    lastIdx = 0
  else:
    lastIdx = int(lastIdx)
  # [[ 3.2. CountUp Idx ]]
  Idx = lastIdx + 1
  if Idx > maxRecord:
    conn.rollback()
    lock.release()
    return False

  # [[[ 4. Insert Last Record ]]]
  c.execute("insert into Book values("+
    str(BookId) + "," +
    str(Idx) + "," +
    "\"" + path + "\"," +
    "\"" + user + "\"," +
    "\"" + comment + "\"," +
    str(int(visible)) + "," +
    "\"" + duration + "\"," +
    str(int(dummy)) + ")")

  # [[[ 5. UnLock ]]]
  conn.commit()
  lock.release()

  return True

# Delete Record
def Delete(
      bookId # Int(In) : BookId
    ): # Bool : True(Success) / False(Failure)
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("begin")
 
  # [[[ 2. Check Exist ]]]
  c.execute("select * from Book " +
    "where BookId = " + str(bookId))
  if c.fetchone() is None:
    # < No Record >
    conn.rollback()
    lock.release()
    return False

  # [[[ 3. Get Delete Idx ]]]
  c.execute("select Idx from Book " +
    "where BookId = " + str(bookId))
  deleteIdx = int(c.fetchone()[0])

  # [[[ 4. Get Max Idx ]]]
  c.execute("select max(Idx) from Book")
  maxIdx = int(c.fetchone()[0])

  # [[[ 5. Delete Record ]]]
  c.execute("delete from Book " +
    "where Bookid = " + str(bookId))

  # [[[ 6. Update Idx after Delete Record ]]]
  updateIdx = deleteIdx + 1
  while updateIdx <= maxIdx:
    c.execute("update Book set " +
      "Idx = " + str(updateIdx-1) + " " +
      "where Idx = " + str(updateIdx))
    updateIdx = updateIdx + 1

  # [[[ 7. UnLock ]]] 
  conn.commit()
  lock.release()

  return True

# List Records
def List(): # list(tuple(BookId,Idx,Path,User,Comment,Visible))
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("begin")

  # [[[ 2. Initialize List ]]]
  list = []

  # [[[ 3. Make List ]]]
  for row in c.execute("select * from Book order by Idx asc"):
    list.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))

  # [[[ 4. UnLock ]]]
  conn.rollback()
  lock.release()
  return list

# Swap Records
def Swap(
      srcBookId, # Int(In) : Src BookId
      dstBookId  # Int(In) : Dst BookId
    ): # Bool : True(Success) / False(Failure)
  global conn
  global c
  global lock
  # [[[ 1. Check Param ]]]
  if srcBookId == dstBookId:
    return False

  # [[[ 0. Lock ]]]
  lock.acquire()
  c.execute("begin")

  # [[[ 1. Check BookId ]]]
  c.execute("select Idx from Book " +
    "where BookId = " + str(srcBookId))
  srcIdx = c.fetchone()
  if srcIdx is None:
    conn.rollback()
    lock.release()
    return False
  c.execute("select Idx from Book " +
    "where BookId = " + str(dstBookId))
  dstIdx = c.fetchone()
  if dstIdx is None:
    conn.rollback()
    lock.release()
    return False
  srcIdx = srcIdx[0]
  dstIdx = dstIdx[0]

  # [[[ 2. Update Idx ]]]
  c.execute("update Book " +
    "set Idx = " + str(-1) + " " +
    "where BookId = " + str(dstBookId))
  c.execute("update Book " +
    "set Idx = " + str(dstIdx) + " " +
    "where Bookid = " + str(srcBookId))
  c.execute("update Book " +
    "set Idx = " + str(srcIdx) + " " +
    "where BookId = " + str(dstBookId))
 
  # [[[ 3. UnLock ]]]
  conn.commit()
  lock.release()

  return True

# Get Playlist Tags
def Playlist(user):
  list = ''
  for row in List():
    list = list + \
      "<li><a href=\"reserve?user=" + \
      user + \
      "&bookId=" + \
      str(row[0]) + \
      "\" rel=\"external\">" + \
      os.path.basename(row[2]) + \
      "</a></li>"
  return list

# Get Total Reserve Time
def GetTotalReserveTime():
  ms = 0 # [10ms]
  for row in List():
    val = re.split('[:.]',row[6])
    ms += int(val[0])*100*60*60
    ms += int(val[1])*100*60
    ms += int(val[2])*100
    ms += int(val[3])
  hour = int(ms/(100*60*60))
  minute = int(ms%(100*60*60)/(100*60))
  second = int(ms%(100*60)/(100))
  ms = int(ms%100)
  return \
    str(hour).zfill(2)+":"+\
    str(minute).zfill(2)+":"+\
    str(second).zfill(2)+"."+\
    str(ms).zfill(2)

# Get Reserve Detail
def ReserveDetail(id):
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("begin")

  # [[[ 2. Query ]]]
  for row in c.execute("select * from Book where BookId = " + id):
    list = row[3] + "<br>" + row[2] + "<br>" + row[6] + "<br>"

  # [[[ 3. UnLock ]]]
  conn.rollback()
  lock.release()
  
  return list

# Reset DB
def Reset():
  global conn
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()

  # [[[ 2. Close ]]]
  if conn is not None:
    conn.close()

  # [[[ 3. Delete DB ]]]
  if os.path.exists("./" + fileName):
    os.remove(fileName)

  # [[[ 4. Initialize DB ]]]
  init()

  # [[[ 5. Unlock ]]]
  lock.release()

init()