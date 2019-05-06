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

from datetime import datetime
import os
import threading

fileName = "favorite.db" # DB File Name
conn = None              # SQLite Connection
c = None                 # SQLite Cursor
lock = threading.Lock()  # Lock Object

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
  c.execute("SELECT * FROM sqlite_master " +
    "WHERE type='table' AND name='Favorite'")
  if c.fetchone() is None:
    # < No Table >
    # [ 1.2.1. Create Favorite Table ]
    c.execute("CREATE TABLE [Favorite] " + 
      "(" +
      "[DirName] TEXT NOT NULL, " +
      "[User] TEXT, " +
      "[FileName] TEXT, " +
      "[Idx] INTEGER NOT NULL," +
      "UNIQUE([User],[Idx]));")

# Add
def Add(
      dirName,  # String(In): Full Path
      fileName, # String(In): File Name
      user      # String(In): User Name 
    ): # Bool True(Success) / False(Failure)
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("BEGIN")

  # [[[ 2. Calc Idx ]]]
  c.execute("SELECT MAX(Idx) from Favorite")
  idx = c.fetchone()[0]
  if None is idx:
    # < Record is None >
    idx = 1
  else:
    # < Record is Exist >
    idx = int(idx) + 1

  # [[[ 3. Check Already Exist ]]]
  c.execute( \
    "SELECT COUNT(Idx) from Favorite WHERE " + \
    "User = ? and DirName = ? and FileName = ?", \
    [user, dirName, fileName])
  exist = c.fetchone()[0]
  if 0 != exist:
    # < Already Exist >
    conn.rollback()
    lock.release()
    return False

  # [[[ 4. Insert Last Record ]]]
  c.execute("INSERT INTO Favorite VALUES("+
    "\"" + dirName + "\"," +
    "\"" + user + "\"," +
    "\"" + fileName + "\", " +
    str(idx) + ")")

  # [[[ 5. UnLock ]]]
  conn.commit()
  lock.release()

  return True

# Get
def Get(
      user, # String(In): User
      idx   # String(In): Idx
    ): # Tuple of (DirName, FileName)
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("BEGIN")

  # [[[ 2. Get DirName and FileName ]]]
  c.execute( \
    "SELECT DirName, FileName FROM Favorite " + \
    "WHERE User = ? AND Idx = ?", \
    [user, idx])

  row = c.fetchone()
  conn.rollback()

  # [[[ 3. Unlock ]]]
  lock.release()

  return row[0], row[1]

# List Records
def List(
      user # String(In): User
    ): # list(tuple(DirName,FileName,Idx))
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("BEGIN")

  # [[[ 2. Initialize List ]]]
  list = []

  # [[[ 3. Make List ]]]
  for row in c.execute( \
    "SELECT DirName,FileName,Idx FROM Favorite WHERE User = ? ORDER BY Idx DESC", \
    [user]):
    list.append((row[0],row[1],row[2]))

  # [[[ 4. UnLock ]]]
  conn.rollback()
  lock.release()
  return list

# Get Favorite List Tags
def FavoriteList(
      user # String(In): User
    ): # String(html tag)
  list = ''
  for row in List(user):
    list = list + \
      "<li>" + \
      "<a href=\"favorite" + \
      "?user=" + user + \
      "&idx=" + str(row[2]) + \
      "\" rel=\"external\">" + \
      row[1] + \
      "</a>" + \
      "</li>"
  return list

# Delete Favorite
def Delete(
      user, # String(In): User
      idx   # String(In): Idx
    ): # None
  global conn
  global c
  global lock
  # [[[ 1. Lock ]]]
  lock.acquire()
  c.execute("BEGIN")

  # [[[ 2. Delete Record ]]]
  c.execute( \
    "DELETE FROM Favorite WHERE " + \
    "User = ? AND Idx = ?", \
    [user,idx])

  # [[[ 3. Unlock ]]]
  lock.release()

# Reset Favorite
def Reset(): # None
  global lock
  global conn
  # [[[ 1. Lock ]]]
  lock.acquire()

  # [[[ 2. Close ]]]
  if conn is not None:
    conn.close()

  # [[[ 3. Delete Favorite File ]]]
  if os.path.exists("." + os.path.sep + fileName):
    os.remove(fileName)

  # [[[ 4. Initialize Favorite File ]]]
  init()

  # [[[ 5. Unlock ]]]
  lock.release()

init()
