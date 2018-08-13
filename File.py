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
import sqlite3
import os
import VideoInfo
fileName = "file.db"
limit = 20
lock = threading.Lock()
conn = None
c = None

def recFiles(directories):
  for root, dirs, files in os.walk(directories):
    for file in files:
      if file[-4:] == ".avi" or file[-4:] == ".mp4":
        yield (file,root)

# Count hit number for keyword
def Count(keywords): # string with <li></li> elements
  global conn
  global lock
  global c
  # [[[ 1. Lock ]]]
  lock.acquire()
  # [[[ 2. Check DB File ]]]
  if not os.path.exists("./" + fileName):
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
  if keywords == "":
    # < All List >
    sql = 'SELECT COUNT(FileID) FROM File'
  else:
    # < Search List >
    for keyword in keywords.split():
      if 1 == isMultiKeyword:
        sql = sql + " AND "
      sql = sql + \
        '(DirName LIKE \'%' + keyword + \
        '%\' OR FileName LIKE \'%' + keyword + '%\')'
      isMultiKeyword = 1
  # [[ 4.2. Query ]]
  for row in c.execute(sql):
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

# Search keyword
def Search(keywords,user,page): # string with <li></li> elements
  global lock
  global conn
  global c
  # [[[ 1. Lock ]]]
  lock.acquire()
  # [[[ 2. Check DB File ]]]
  if not os.path.exists("./" + fileName):
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
  sql = 'SELECT FileID, FileName FROM File WHERE '
  isMultiKeyword = 0
  keywords = keywords.strip()
  if keywords == "":
    # < All List >
    sql = 'SELECT FileID, FileName FROM File'
  else:
    # < Search List >
    for keyword in keywords.split():
      if 1 == isMultiKeyword:
        sql = sql + " AND "
      sql = sql + \
        '(DirName LIKE \'%' + keyword + \
        '%\' OR FileName LIKE \'%' + keyword + '%\')'
      isMultiKeyword = 1
  sql = sql + " LIMIT " + str(limit)
  sql = sql + " OFFSET " + str(limit * (int(page)-1))
  # [[ 4.2. Query ]]
  for row in c.execute(sql):
    list = list + \
      "<li><a href=\"detail?fileId=" + str(row[0]) + \
      "&user=" + user + "&keyword=" + keywords + \
      "&page=" + page + "\" rel=\"external\">" + \
      row[1] + "</a></li>"
  # [[[ 5. Unlock ]]]
  lock.release()
  return list

# Detail
def Detail(no,user): # string html
  global lock
  global conn
  global c
   # [[[ 1. Lock ]]]
  lock.acquire()
  # [[[ 2. Prepare SQLite ]]]
  if conn is None:
    conn = sqlite3.connect(fileName, check_same_thread=False)
    c = conn.cursor()
  # [[[ 3. Make <li></li> List ]]]
  list = '' # return html string
  # [[ 3.1. Prepare SQL statement ]]
  sql = 'SELECT FileID, DirName, FileName, Size FROM File WHERE FileID = ' + no
  # [[ 3.2. Query ]]
  size = 0
  filePath = ''
  for row in c.execute(sql):
    size = row[3]
    filePath = os.path.join(row[1],row[2])
  # [[[ 4. Unlock ]]]
  lock.release()
  # [[[ 5. Make Tag ]]]
  list = filePath + "<br>" + "{:,}".format(size) + "[Byte]<br>"
  list = list + VideoInfo.GetDuration(filePath)
  return list

# Delete DB
def Delete():
  global conn
  # [[[ 1. Close DB ]]]
  if conn is not None:
    conn.close
  # [[[ 2. Delete DB ]]]
  if os.path.exists("./" + fileName):
    os.remove(fileName)
 
# Initialize DB
def init():
  global lock
  global conn
  global c
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
    "PRIMARY KEY(FileID)" +
    ");")
  # [[[ 5. Insert File Information ]]]
  fileId = 0
  for row in recFiles('/media/pi/'):
    c.execute("insert into File values(" +
      str(fileId) + "," +
      "\"" + row[1] + "\"" + "," +
      "\"" + row[0] + "\"" + "," +
      str(os.path.getsize(os.path.join(row[1],row[0]))) + ")")
    fileId = fileId + 1
  conn.commit()
  # [[[ 6. Unlock ]]]
  lock.release()
