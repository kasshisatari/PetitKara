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

@app.get("/console")
def console():
  global path
  global user
  global comment
  global pause
  global duration
  if len(Book.List()) != 0 and pause is False:
    if Video.CheckPlaying() is False:
      bookList = Book.List()[0]
      path = bookList[2]
      user = bookList[3]
      comment = bookList[4]
      dummy = bookList[7]
      duration = VideoInfo.GetDuration(path)
      if dummy == 0:
        Video.Open(path, vol)
        History.Add(path, user, comment)
        pause = False
      else:
        HDMI.Switch()
        pause = True
      bookId = bookList[0]
      Book.Delete(bookId)

  if Video.CheckPlaying() is False:
    path = None
    user = None
    comment = None
    duration = None
  
  return template('console')

@app.get("/shutdown")
def shutdown():
  os.system("sudo shutdown -h now")
  redirect("/")

@app.get("/restart")
def restart():
  os.system("sudo shutdown -r now")
  redirect("/")

@app.get("/current")
def current():
  if Video.CheckPlaying() is False:
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

@app.get("/stop")
def stop():
  Video.Stop()
  redirect( \
    request.query.back + \
    "?name=" + request.query.user + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookId)

@app.get("/pause")
def suspend():
  global pause
  if pause is True and Video.CheckPlaying() is False:
    HDMI.Switch()
  Video.Pause()
  if pause is False:
    if Video.CheckPlaying() is False:
      HDMI.Switch()
    pause = True
  else:
    pause = False
  redirect( \
    "/current?user=" + request.query.user + \
    "&back=" + request.query.back + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&bookId=" + request.query.bookid)

@app.get("/audio")
def audio():
  Video.SwitchAudio()
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

HDMI.init()
img = qrcode.make("http://"+Address.Getwlan0()+":8080/")
img.save("static/toppage.png")
web.serve(app,host="0.0.0.0",port=8080)
