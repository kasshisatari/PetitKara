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

import threading
import sqlite3
import os
from datetime import datetime
import History

# Check Raspbian
def CheckRaspbian():
  flag = False
  filePath = os.path.sep + "etc" + os.path.sep + "issue"
  if False is os.path.exists(filePath):
    return False
  issue = open(filePath)
  for line in issue:
    if 0 == line.find("Raspbian"):
      flag = True
  issue.close()
  return flag

# Check Windows
def CheckWindows():
  flag = False
  if 0 == os.name.find("nt"):
    flag = True
  return flag

if True is CheckRaspbian():
  from Raspi import VideoInfo
  from Raspi import System
elif True is CheckWindows():
  from Win import VideoInfo
  from Win import System
  pass

fileName = "file.db"    # DB File Name  
limit = 20              # Max Search Record Per Page
lock = threading.Lock() # Lock Object
conn = None             # SQLite Connection
c = None                # SQLite Cursor
videoInfo = None        # videoInfo instance
system = None           # system instance

# Get FileId
def GetFileId(
      dirName, # String(In): Full path
      filename # String(In): File Name
    ): # String(FileId) / None
  global conn
  global lock
  global c
  # [[[ 1. Lock ]]]
  lock.acquire()

  # [[[ 2. Check DB File ]]]
  if not os.path.exists("." + os.path.sep + fileName):
    # < File not Exists >
    lock.release()
    return None

  # [[[ 3. Prepare SQLite ]]]
  if None is conn:
    conn = sqlite3.connect(fileName, check_same_thread=False)
    c = conn.cursor()

  # [[[ 4. Get FileId ]]]
  c.execute( \
    "SELECT FileId FROM File WHERE DirName = ? AND FileName = ?", \
    [dirName, filename])
  fileId = c.fetchone()[0]

  # [[[ 5. Unlock ]]]
  lock.release()

  return fileId

# Get movie file path
def recFiles(directories): # string for filepath
  for directory in directories:
    for root, dirs, files in os.walk(directory):
      for file in files:
        if -1 != root.find(os.path.sep + '$RECYCLE.BIN' + os.path.sep):
          continue
        if   file[-4:] == ".avi" \
          or file[-4:] == ".mp4" \
          or file[-4:] == ".flv" \
          or file[-4:] == ".mkv":
          yield (file,root)

# Get file information from FileID
def Get(
      fileId # Integer(In): FileID
    ): # Tuple of (Directory Name, File Name)
  global conn
  global lock
  global c
  # [[[ 1. Lock ]]]
  lock.acquire()
  # [[[ 2. Check DB File ]]]
  if not os.path.exists("." + os.path.sep + fileName):
    # < File not Exists >
    lock.release()
    return "","" 
  # [[[ 3. Prepare SQLite ]]]
  if conn is None:
    conn = sqlite3.connect(fileName, check_same_thread=False)
    c = conn.cursor()
  # [[[ 4. Get Directory Name and File Name ]]]
  c.execute(
    "SELECT DirName, FileName FROM File WHERE FileID = ?", \
    [fileId])
  row = c.fetchone()
  # [[[ 5. Unlock ]]]
  lock.release()
  return row[0],row[1]

# Count hit number for keyword
def Count(keywords): # string with <li></li> elements
  global conn
  global lock
  global c
  # [[[ 1. Lock ]]]
  lock.acquire()
  # [[[ 2. Check DB File ]]]
  if not os.path.exists("." + os.path.sep + fileName):
    # < File not Exists >
    lock.release()
    return "0"
  # [[[ 3. Prepare SQLite ]]]
  if conn is None:
    conn = sqlite3.connect(fileName, check_same_thread=False)
    c = conn.cursor()
  # [[[ 4. Count hit number ]]]
  count = '' # return count string
  # [[ 4.1. Prepare SQL statement ]]
  sql = 'SELECT COUNT(FileID) FROM File WHERE '
  isMultiKeyword = 0
  keywords = keywords.strip()
  param = []
  if keywords == "":
    # < All List >
    sql = 'SELECT COUNT(FileID) FROM File'
  else:
    # < Search List >
    for keyword in keywords.split():
      if 1 == isMultiKeyword:
        sql = sql + " AND "
      sql = sql + \
        '(DirName LIKE ? OR FileName LIKE ?)'
      isMultiKeyword = 1
      param = param \
        + [ "%" + keyword + "%" , "%" + keyword + "%" ]
  # [[ 4.2. Query ]]
  for row in c.execute(sql,param):
    count = row[0]
  # [[[ 5. Unlock ]]]
  lock.release()
  return count

# Page Link
def Page(keywords, user): # string with <a></a> elements
  count = int(Count(keywords))
  maxPage = int((count - 1) / limit + 1)
  list = ''
  for i in range(maxPage):
    list = list + \
      "<a href=\"list?user=" + user + \
      "&page=" + str(i+1) + "&keyword=" + \
      keywords + "\" rel=\"external\">" + str(i+1) + "</a>"
  return list

# Navigate Link
def Navi(keywords, user, page): # string with <a></a> elements
  # [[[ 1. Get Page Count ]]]
  count = int(Count(keywords))

  # [[[ 2. Get Page Numbers ]]]
  maxPage = int((count - 1) / limit + 1)
  prevPage = int(page) - 1
  nextPage = int(page) + 1

  # [[[ 3. Return Navigate Link ]]]
  if 0 == count or \
     (0 == prevPage and \
     maxPage + 1 == nextPage):
    # < No Next and Previous Page >
    return ""
  elif 0 == prevPage:
    # < No Previous Page >
    return  \
      u"<a href=\"list?user=" + user + \
      u"&page=" + str(nextPage) + \
      u"&keyword=" + keywords + \
      u"\" rel=\"external\">次へ</a><br>"
  elif maxPage + 1 == nextPage:
    # < No Next Page >
    return \
      u"<a href=\"list?user=" + user + \
      u"&page=" + str(prevPage) + \
      u"&keyword=" + keywords + \
      u"\" rel=\"external\">前へ</a><br>"
  else:
    # < Previous and Next Page >
    return \
      u"<a href=\"list?user=" + user + \
      u"&page=" + str(prevPage) + \
      u"&keyword=" + keywords + \
      u"\" rel=\"external\">前へ</a>" + \
      u"<a href=\"list?user=" + user + \
      u"&page=" + str(nextPage) + \
      u"&keyword=" + keywords + \
      u"\" rel=\"external\" class=\"ui-btn-right\">次へ</a><br>"

# Search keyword
def Search(keywords,user,page): # string with <li></li> elements
  global lock
  global conn
  global c

  # [[[ 1. Lock ]]]
  lock.acquire()

  # [[[ 2. Check DB File ]]]
  if not os.path.exists("." + os.path.sep + fileName):
    # < File not Exists >
    lock.release()
    return ""

  # [[[ 3. Prepare SQLite ]]]
  if conn is None:
    conn = sqlite3.connect(fileName, check_same_thread=False)
    c = conn.cursor()

  # [[[ 4. Make <li></li> List ]]]
  list = '' # return html string
  # [[ 4.1. Prepare SQL statement ]]
  sql = 'SELECT FileID, FileName, DirName FROM File WHERE '
  isMultiKeyword = 0
  keywords = keywords.strip()
  param = []
  if keywords == "":
    # < All List >
    sql = 'SELECT FileID, FileName, DirName FROM File'
  else:
    # < Search List >
    for keyword in keywords.split():
      if 1 == isMultiKeyword:
        sql = sql + " AND "
      sql = sql + \
        '(DirName LIKE ? OR FileName LIKE ?)'
      isMultiKeyword = 1
      param = param \
        + [ "%" + keyword + "%" , "%" + keyword + "%" ]
  sql = sql + " ORDER BY FileName ASC LIMIT " + str(limit)
  sql = sql + " OFFSET " + str(limit * (int(page)-1))
  # [[ 4.2. Query ]]
  for row in c.execute(sql,param):
    filePath = os.path.join(row[2],row[1])
    if 0 != History.Count(filePath):
      # < Already Play >
      list = list + \
        "<li><a class=\"ui-btn ui-icon-check ui-btn-icon-left\" " + \
        "href=\"detail?fileId=" + str(row[0]) + \
        "&user=" + user + "&keyword=" + keywords + \
        "&page=" + page + "\" rel=\"external\"><font style=\"white-space:normal;\">" + \
        row[1] + "</font></a></li>"
    else:
      # < Not Play >
      list = list + \
        "<li><a " + \
        "href=\"detail?fileId=" + str(row[0]) + \
        "&user=" + user + "&keyword=" + keywords + \
        "&page=" + page + "\" rel=\"external\"><font style=\"white-space:normal;\">" + \
        row[1] + "</font></a></li>"

  # [[[ 5. Unlock ]]]
  lock.release()

  return list

# Detail
def Detail(
      no,  # String(In): FileID
      user # String(In): User Name
    ): # String(html)
  global lock
  global conn
  global c
  global videoInfo

   # [[[ 1. Lock ]]]
  lock.acquire()

  # [[[ 2. Prepare SQLite ]]]
  if conn is None:
    conn = sqlite3.connect(fileName, check_same_thread=False)
    c = conn.cursor()

  # [[[ 3. Make <li></li> List ]]]
  list = '' # return html string
  # [[ 3.1. Prepare SQL statement ]]
  sql = 'SELECT FileID, DirName, FileName, Size, Time FROM File WHERE FileID = ?'
  # [[ 3.2. Query ]]
  size = 0
  time = ''
  filePath = ''
  for row in c.execute(sql, [no]):
    size = row[3]
    time = row[4]
    filePath = os.path.join(row[1],row[2])

  # [[[ 4. Unlock ]]]
  lock.release()

  # [[[ 5. Make Tag ]]]
  list = filePath + "<br>" + "{:,}".format(size) + "[Byte]<br>"
  list = list + time + "<br>"
  if None is videoInfo:
    videoInfo = VideoInfo.VideoInfo()
  if (None is videoInfo.GetDuration(filePath)):
    list = u"動画が見つかりません。" + "<br>" + u"曲情報を更新してください。"
  else:
    list = list + videoInfo.GetDuration(filePath)
    # [[ 5.1. History Count ]]
    list = list + "<br>" + str(History.Count(filePath)) + u"回"

  return list

# CheckFile
def CheckFile(no): # Exist(True) / Not Exist(False)
  global lock
  global conn
  global c
   # [[[ 1. Lock ]]]
  lock.acquire()
  # [[[ 2. Prepare SQLite ]]]
  if conn is None:
    conn = sqlite3.connect(fileName, check_same_thread=False)
    c = conn.cursor()
  # [[[ 3. Prepare SQL statement ]]]
  sql = 'SELECT FileID, DirName, FileName, Size FROM File WHERE FileID = ?'
  # [[[ 4. Query ]]]
  filePath = ''
  for row in c.execute(sql, [no]):
    filePath = os.path.join(row[1],row[2])
  # [[[ 5. Unlock ]]]
  lock.release()
  # [[[ 6. CheckFile ]]]
  if not os.path.exists(filePath):
    # < File not Exists >
    return False
  else:
    # < File Exists >
    return True

# Delete DB
def Delete(): # None
  global conn
  # [[[ 1. Close DB ]]]
  if conn is not None:
    conn.close
  # [[[ 2. Delete DB ]]]
  if os.path.exists("." + os.path.sep + fileName):
    os.remove(fileName)
 
# Initialize DB
def init(): # None
  global lock
  global conn
  global c
  global system
  # [[[ 1. Lock ]]]
  lock.acquire()
  # [[[ 2. Delete DB ]]]
  Delete()
  # [[[ 3. Prepare SQLite ]]]
  conn = sqlite3.connect(fileName, check_same_thread=False)
  c = conn.cursor()
  # [[[ 4. Create Table ]]]
  c.execute("begin")
  c.execute("CREATE TABLE [File] " +
    "([FileID] INTEGER NOT NULL UNIQUE," +
    "[DirName] TEXT NOT NULL," +
    "[FileName] TEXT NOT NULL," +
    "[Size] INTEGER," +
    "[Time] TEXT NOT NULL," +
    "PRIMARY KEY(FileID)" +
    ");")
  # [[[ 5. Insert File Information ]]]
  fileId = 0
  if None is system:
    system = System.System()
  for row in recFiles(system.GetDir()):
    c.execute("insert into File values(" +
      str(fileId) + "," +
      "\"" + row[1] + "\"" + "," +
      "\"" + row[0] + "\"" + "," +
      str(os.path.getsize(os.path.join(row[1],row[0]))) + "," +
      "\"" + datetime.fromtimestamp(os.stat(os.path.join(row[1],row[0])).st_mtime).strftime("%Y/%m/%d %H:%M:%S") + "\")")
    fileId = fileId + 1
  conn.commit()
  # [[[ 6. Unlock ]]]
  lock.release()


# GetAudioTag
def GetAudioTag(
      no  # String(In): FileID
    ): # String(html)
  global lock
  global conn
  global c
  global videoInfo

   # [[[ 1. Lock ]]]
  lock.acquire()

  # [[[ 2. Prepare SQLite ]]]
  if conn is None:
    conn = sqlite3.connect(fileName, check_same_thread=False)
    c = conn.cursor()

  # [[[ 3. Make <li></li> List ]]]
  list = '' # return html string
  # [[ 3.1. Prepare SQL statement ]]
  sql = 'SELECT FileID, DirName, FileName, Size, Time FROM File WHERE FileID = ?'
  # [[ 3.2. Query ]]
  size = 0
  time = ''
  filePath = ''
  for row in c.execute(sql, [no]):
    size = row[3]
    time = row[4]
    filePath = os.path.join(row[1],row[2])

  # [[[ 4. Unlock ]]]
  lock.release()

  # [[[ 5. Make Tag ]]]
  return videoInfo.GetAudioTag(filePath)

