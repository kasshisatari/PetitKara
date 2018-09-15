# -*- coding: utf-8 -*-

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

from bottle import \
  Bottle, run, get, template, \
  request, route, static_file, redirect
from paste import httpserver as web
import sqlite3
import os
import subprocess
import Book
import History
import File
import Address
import qrcode
import VideoInfo
import HDMI
import Video

path = None     # playing file path
user = None     # playing file user
comment = None  # playing file comment
duration = None # playing file duration
vol = -2100     # current volume
volStep = 300   # 0.3dB
app = Bottle()  # bottle instance
pause = False   # pause

# Monitor View
@app.get("/console")
def console():
  global path
  global user
  global comment
  global pause
  global duration

  # [[[ 1. Update Playing Video ]]] 
  if 0 != len(Book.List()) and False is pause:
    # < Can Play >
    if False is Video.CheckPlaying():
      # < Not Playing >
      # [[ 1.1. Get and Update First Reservation ]]
      bookList = Book.List()[0]
      path = bookList[2]
      user = bookList[3]
      comment = bookList[4]
      dummy = bookList[7]
      duration = VideoInfo.GetDuration(path)
      # [[ 1.2. Check Dummy ]]
      if 0 == dummy:
        # < Not Dummy >
        # [ 1.2.1. Play Video ]
        Video.Open(path, vol)
        # [ 1.2.2. Add History ]
        History.Add(path, user, comment)
        # [ 1.2.3. Update pause status for playing ]
        pause = False
      else:
        # < Dummy >
        # [ 1.2.4. Switch HDMI Signal ]
        HDMI.Switch()
        # [ 1.2.5. Update pause status for pausing ]
        pause = True
      # [[ 1.3. Delete Playing Book ]]
      Book.Delete(bookList[0])

  # [[[ 2. Update View ]]]
  return template('console')

# Shutdown OS
@app.get("/shutdown")
def shutdown():
  # [[[ 1. Shutdown ]]]
  os.system("sudo shutdown -h now")

# Restart OS
@app.get("/restart")
def restart():
  # [[[ 1. Restart ]]]
  os.system("sudo shutdown -r now")

# Remote-Controller View
@app.get("/current")
def current():
  # [[[ 1. Update View ]]]
  if False is Video.CheckPlaying():
    # < Not Playing >
    # [[ 1.1. Not Playing View ]]]
    return template( \
      'nothing', \
      name = request.query.user, \
      vol = vol/100, \
      back = request.query.back, \
      keyword = request.query.keyword, \
      page = request.query.page, \
      fileId = request.query.fileId, \
      bookId = request.query.bookId, \
      pause = u"再開" if pause is True else u"一時停止")
  else:
    # < Playing >
    # [[ 1.2. Playing View ]]
    return template( \
      'current', \
      name = request.query.user, \
      user = user, \
      path = path, \
      comment = comment, \
      duration = duration, \
      back = request.query.back, \
      keyword = request.query.keyword, \
      page = request.query.page, \
      fileId = request.query.fileId, \
      bookId = request.query.bookId, \
      vol = vol/100)

# Stop Video
@app.get("/stop")
def stop():
  # [[[ 1. Stop Video ]]]
  Video.Stop()

  # [[[ 2. Redirect Previous View ]]]
  redirect( \
    request.query.back + \
    "?name=" + request.query.user + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookId)

# Pause Video
@app.get("/pause")
def suspend():
  global pause
  # [[[ 1. Switch HDMI Signal ]]]
  if True is pause and False is Video.CheckPlaying():
    # < Pausing >
    HDMI.Switch()

  # [[[ 2. Pause Video ]]]
  Video.Pause()

  # [[[ 3. Switch HDMI Signal to Other Component ]]]
  if False is pause:
    # < Not Pausing >
    if False is Video.CheckPlaying():
      # < Not Playing >
      HDMI.Switch()
    # [[ 3.1. Update Pause Status Not Pausing -> Pausing ]]
    pause = True
  else:
    # [[ 3.2. Update Pause Status Pausing -> Not Pausing ]]
    pause = False

  # [[[ 4. Redirect Remote-Controller View ]]]
  redirect( \
    "/current?user=" + request.query.user + \
    "&back=" + request.query.back + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookid)

# Switch Audio of Video
@app.get("/audio")
def audio():
  # [[[ 1. Switch Audio ]]]
  Video.SwitchAudio()

  # [[[ 2. Redirect Remote-Controller View ]]]
  redirect( \
    "/current?user=" + request.query.user + \
    "&back=" + request.query.back + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookid)

@app.get("/rew")
def rew():
  Video.Rewind()
  redirect( \
    "/current?user=" + request.query.user + \
    "&back=" + request.query.back + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookid)

@app.get("/ff")
def ff():
  Video.FastForward()
  redirect( \
    "/current?user=" + request.query.user + \
    "&back=" + request.query.back + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookid)

@app.get("/down")
def down():
  global vol
  vol = vol - volStep
  Video.DownVolume()
  redirect( \
    "/current?user=" + request.query.user + \
    "&back=" + request.query.back + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookid)

@app.get("/up")
def up():
  global vol
  vol = vol + volStep
  Video.UpVolume()
  redirect( \
    "/current?user=" + request.query.user + \
    "&back=" + request.query.back + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookid)

@app.route('/static/:path#.+#', name='static')
def static(path):
  return static_file(path, root='static')

@app.get("/")
def top():
  return template('top')

@app.get("/search")
def search():
  return template( \
    'search', \
    name = request.query.user, \
    keyword = request.query.keyword)

@app.get("/list")
def listpage():
  return template( \
    'list', \
    name = request.query.user, \
    keyword = request.query.keyword, \
    page=request.query.page)

@app.get("/history")
def history():
  return template( \
    'history', \
    name = request.query.user)

@app.get("/insert")
def insert():
  fileId = request.query.get('fileId')
  visible = request.query.get('secret')
  if ("on"==visible):
    visible = False
  else:
    visible = True
  dirName, fileName = File.Get(fileId)
  Book.AddTop( \
    os.path.join(dirName,fileName), \
    request.query.user, \
    request.query.comment, \
    visible, \
    VideoInfo.GetDuration(os.path.join(dirName,fileName)), \
    False)
  redirect( \
    "/list?user=" + request.query.user + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page)

@app.get("/playlist")
def playlist():
  return template( \
    'playlist', \
    name = request.query.user)

@app.get("/delete")
def delete():
  Book.Delete(int(request.query.bookId))
  redirect( \
    "/playlist?user=" + request.query.user)

@app.get("/reserve")
def reserve():
  return template( \
    'reserve', \
    name = request.query.user, \
    id = request.query.bookId)

@app.get("/moveup")
def moveup():
  Book.MoveUp(request.query.bookId)
  redirect( \
    "/playlist?" + \
    "user=" + request.query.user)

@app.get("/movedown")
def movedown():
  Book.MoveDown(request.query.bookId)
  redirect( \
    "/playlist?" + \
    "user=" + request.query.user)

@app.get("/add")
def add():
  fileId = request.query.get('fileId')
  visible = request.query.get('secret')
  if ("on"==visible):
    visible = False
  else:
    visible = True
  dirName, fileName = File.Get(fileId)
  Book.AddLast( \
    os.path.join(dirName,fileName), \
    request.query.user, \
    request.query.comment, \
    visible, \
    VideoInfo.GetDuration(os.path.join(dirName,fileName)), \
    False)
  redirect( \
    "/list?user=" + request.query.user + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page)

@app.get("/dummy")
def dummy():
  Book.AddLast( \
    u"空予約", \
    request.query.user, \
    "", \
    True, \
    "00:00:00.00", \
    True)
  redirect( \
    "/search?user=" + request.query.user + \
    "&keyword=" + request.query.keyword)

@app.get("/detail")
def detail():
  if (True is File.CheckFile(request.query.fileId)):
    return template( \
      'detail', \
      name = request.query.user, \
      id = request.query.fileId, \
      keyword = request.query.keyword, \
      page=request.query.page)
  else:
    return template( \
      'novideo', \
      name = request.query.user, \
      id = request.query.fileId, \
      keyword = request.query.keyword, \
      page=request.query.page)

@app.get("/refresh")
def refresh():
  File.init()
  redirect("/")

@app.get("/reset")
def reset():
  Book.Reset()
  File.Delete()
  History.Delete()
  redirect("/")

@app.get("/initHistory")
def refresh():
  History.Delete()
  redirect("/")

# [[[ 1. Initialize HDMI Signal Switcher ]]]
HDMI.init()

# [[[ 2. Make QR-Code ]]]
img = qrcode.make("http://"+Address.Getwlan0()+":8080/")
img.save("static/toppage.png")

# [[[ 3. Start Web Server ]]]
web.serve(app,host="0.0.0.0",port=8080)
