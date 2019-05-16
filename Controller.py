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

import os
import re
import datetime
import threading
from bottle import \
  Bottle, run, get, template, \
  request, route, static_file, redirect, \
  response
from paste import httpserver as web
import qrcode
import Book
import History
import File
import Favorite

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
  from Raspi import Network
  from Raspi import VideoInfo
  from Raspi import HDMI
  from Raspi import Video
  from Raspi import System
elif True is CheckWindows():
  from Win import Network
  from Win import VideoInfo
  from Win import HDMI
  from Win import Video
  from Win import System
  pass

path = None             # playing file path
user = None             # playing file user
comment = None          # playing file comment
duration = None         # playing file duration
audioNum = 0            # playing file audio stream
vol = -4500             # current volume
app = Bottle()          # bottle instance
pause = False           # pause
video = None            # video instance
videoInfo = None        # videoInfo instance
network = None          # network Instance
hdmi = None             # hdmi instance
system = None           # system Instance
lock = threading.Lock() # Lock Object

# Monitor View
@app.get("/console")
def console():
  ssid = network.GetSSID()
  password = network.GetPassword()
  return template( \
    'console', \
    ssid=ssid, \
    password=password)

# Play Video
@app.get("/play")
def console():
  global path
  global user
  global comment
  global pause
  global duration
  global audioNum

  # [[[ 1. Update Playing Video ]]] 
  if 0 != len(Book.List()) and False is pause:
    # < Can Play >
    if False is video.CheckPlaying():
      # < Not Playing >
      # [[ 1.1. Lock ]]
      lock.acquire()
      try:
        # [[ 1.2. Get and Update First Reservation ]]
        bookList = Book.List()[0]
        path = bookList[2]
        user = bookList[3]
        comment = bookList[4]
        dummy = bookList[8]
        audioIndex = int(bookList[7])
        duration = videoInfo.GetDuration(path)
        audioNum = videoInfo.GetAudioNum(path)
        # [[ 1.2. Check Dummy ]]
        if 0 == dummy:
          # < Not Dummy >
          # [ 1.2.1. Play Video ]
          video.Open(path, vol, audioNum, audioIndex)
          # [ 1.2.2. Add History ]
          History.Add(path, user, comment)
          # [ 1.2.3. Update pause status for playing ]
          pause = False
        else:
          # < Dummy >
          # [ 1.2.4. Switch HDMI Signal ]
          hdmi.Switch()
          # [ 1.2.5. Update pause status for pausing ]
          pause = True
      except:
        import traceback
        traceback.print_exc()
      finally:
        # [[ 1.3. Delete Playing Book ]]
        Book.Delete(bookList[0])
        # [[ 1.4. Unlock ]]
        lock.release()

# Favorites View
@app.get("/favorites")
def favorites():
  # [[[ 1. Update View ]]]
  return template( \
    'favorites', \
    name = request.query.user)

# Favorite View
@app.get("/favorite")
def favorite():
  # [[[ 1. Get FileId for Book ]]]
  dirName, fileName = \
    Favorite.Get( \
      request.query.user,
      request.query.idx)
  fileId = File.GetFileId(dirName, fileName)

  # [[[ 2. Update View ]]]
  if None is not fileId:
    # < Exist Video File >
    return template( \
      'favorite', \
      name = request.query.user, \
      idx = request.query.idx, \
      id = fileId)
  else:
    # < Not Exist Video File >
    return template( \
      'nofavorite', \
      name = request.query.user, \
      idx = request.query.idx)

# Bookmark
@app.get("/bookmark")
def bookmark():
  # [[[ 1. Get File Path ]]]
  dirName, fileName = File.Get(request.query.fileId)

  # [[[ 2. Add Favorite ]]]
  Favorite.Add(dirName, fileName, request.query.user)

  # [[[ 3. Redirect Search View ]]]
  redirect( \
    "/list?user=" + request.query.user + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page)

# Shutdown OS
@app.get("/shutdown")
def shutdown():
  # [[[ 1. Shutdown ]]]
  system.Shutdown()

# Restart OS
@app.get("/restart")
def restart():
  # [[[ 1. Restart ]]]
  system.Restart()

# Posotion
@app.get("/pos/json")
def posinfo():
  # [[[ 1. Check Playing ]]]
  if False is video.CheckPlaying():
    # < Not Playing >
    # [[ 1.1. Return JSON ]]]
    return "{\"play\":false}"
  # < Playing >
  # [[[ 2. Return JSON ]]]
  return "{\"play\":true,\"pos\":" + str(video.Position()) + "}"

# Remote-Controller View
@app.get("/current/json")
def currentinfo():
  # [[[ 1. Update View ]]]
  pauseStr = "true"
  if False is pause:
    pauseStr = "false"
  if False is video.CheckPlaying():
    # < Not Playing >
    # [[ 1.1. Not Playing View ]]]
    return "{" + \
      "\"play\":false," + \
      "\"vol\":" + str(vol/100) + "," + \
      "\"pause\":" + pauseStr + "}"
  else:
    # < Playing >
    # [[ 1.2. Playing View ]]
    pos = video.Position()
    return "{" + \
      "\"play\":true," + \
      "\"path\":\"" + path.replace("\\", "/") + "\"," + \
      "\"pos\":" + str(video.Position()) + "," + \
      "\"duration\":\"" + duration + "\"," + \
      "\"user\":\"" + user + "\"," + \
      "\"vol\":" + str(vol/100) + "," + \
      "\"pause\":" + pauseStr + "}"

# Remote-Controller View
@app.get("/current")
def current():
  # [[[ 1. Update View ]]]
  return template( \
    'current', \
    name = request.query.user, \
    back = request.query.back, \
    keyword = request.query.keyword, \
    page = request.query.page, \
    fileId = request.query.fileId, \
    bookId = request.query.bookId, \
    time = request.query.time, \
    idx = request.query.idx)

# Stop Video
@app.get("/stop")
def stop():
  global duration

  # [[[ 1. Stop Video ]]]
  video.Stop()
  duration = None

  # [[[ 2. Redirect Previous View ]]]
  redirect( \
    request.query.back + \
    "?user=" + request.query.user + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page + \
    "&fileId=" + request.query.fileId + \
    "&idx=" + request.query.idx + \
    "&time=" + request.query.time + \
    "&bookId=" + request.query.bookId)

# Playing Status
@app.get("/playing/json")
def playing():
  if False is pause:
    return "{\"playing\":false}"
  else:
    return "{\"playing\":true}"

# Pause Video
@app.get("/pause/json")
def suspend():
  global pause
  # [[[ 1. Switch HDMI Signal ]]]
  if True is pause and False is video.CheckPlaying():
    # < Pausing >
    hdmi.Switch()

  # [[[ 2. Pause Video ]]]
  video.Pause()

  # [[[ 3. Switch HDMI Signal to Other Component ]]]
  if False is pause:
    # < Not Pausing >
    if False is video.CheckPlaying():
      # < Not Playing >
      hdmi.Switch()
    # [[ 3.1. Update Pause Status Not Pausing -> Pausing ]]
    pause = True
  else:
    # [[ 3.2. Update Pause Status Pausing -> Not Pausing ]]
    pause = False

  # [[[ 4. Return JSON ]]]
  return playing()

# Switch Audio of Video
@app.get("/audio")
def audio():
  # [[[ 1. Switch Audio ]]]
  video.SwitchAudio()

# Position Video
@app.get("/pos")
def posctrl():
  # [[[ 1. Check Request ]]]
  if "" != request.query.offset:
    # < Change Position >
    if int(request.query.offset) > 0:
      video.FastForward()
    else:
      video.Rewind()

# Volume Control
@app.get("/vol/json")
def volctrl():
  global vol
  # [[[ 1. Check Request ]]]
  if "" != request.query.step:
    # < Change Volume >
    vol = vol + int(request.query.step)
    if int(request.query.step) > 0:
      video.UpVolume()
    else:
      video.DownVolume()

  # [[[ 2. Return JSON ]]]
  return "{\"vol\":" + str(vol/100) + "}"

@app.route('/static/:path#.+#', name='static')
def static(path):
  return static_file(path, root='static')

@app.get("/admin")
def admin():
  configMenu = ""
  if 0 > system.GetHW().find("Win"):
    configMenu = "<a href=\"config\" data-role=\"button\" rel=\"external\">設定</a>"
  return template( \
    'admin', \
    config = configMenu)

@app.get("/")
def top():
  ssid = network.GetSSID()
  password = network.GetPassword()
  return template( \
    'top', \
    ssid = ssid, \
    password = password)

@app.get("/config")
def config():
  if 0 == system.GetHW().find("Raspi:ALSA"):
    port = video.GetCurrentAudioPort()
    rca = "<label for=\"port\">音声出力切替(次の再生から有効)</label>"
    rca += "<select name=\"port\" id=\"port\">"
    if 0 == port.find("HDMI"):
      rca += "<option value=\"0\" selected>HDMI</option>"
      rca += "<option value=\"1\">RCA</option>"
    else:
      rca += "<option value=\"0\">HDMI</option>"
      rca += "<option value=\"1\" selected>RCA</option>"
    rca += "</select>"
  else:
    rca = "<input id=\"port\" name=\"port\" type=\"hidden\" value=\"0\" />"
  return template( \
    'config', \
    password = network.GetPassword(), \
    rca = rca)

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

@app.get("/sync")
def sync():
  now = datetime.datetime.now()
  recv = datetime.datetime.strptime(request.query.time, "%Y/%m/%d %H:%M:%S")
  diff = abs((recv - now).total_seconds())
  if (diff > 10):
    system.SetTime(request.query.time)

@app.get("/history")
def history():
  return template( \
    'history', \
    name = request.query.user)

@app.get("/history/csv")
def historyCsv():
  recv = datetime.datetime.strptime(request.query.time, "%Y/%m/%d %H:%M:%S")
  response.content_type = 'application/octet-stream'
  response.headers['Content-Disposition'] = \
    "attachment; filename=" + \
    recv.strftime('%Y-%m-%d_%H-%M-%S') + ".csv"
  csv = ''
  extractFlag = False
  for row in History.Extract():
    if row[4] == request.query.time:
      extractFlag = True
    if True == extractFlag:
      csv = csv + \
        row[4] + "," + row[0] + "," + \
        row[2] + "," + row[3] + "," + row[1] + "\r\n"
  return csv

@app.get("/deletehistory")
def deleteHistory():
  History.Delete(request.query.time)
  redirect('/history?user=' + request.query.user)

@app.get("/changehistory")
def changeHistory():
  History.Modify(request.query.time, request.query.comment)
  redirect('/history?user=' + request.query.user)

@app.get("/historydetail")
def historyDetail():
  return template( \
    'historydetail', \
    name = request.query.user, \
    time = request.query.time)

@app.get("/historydetail/json")
def historyDetailJson():
  row = History.Get(request.query.time)
  return "{" + \
    "\"path\":\"" + row[0] + "\"," + \
    "\"user\":\"" + row[1] + "\"," + \
    "\"comment\":\"" + row[2] + "\"," + \
    "\"time\":\"" + row[3] + "\"" + \
    "}"

@app.get("/history/json")
def historyJson():
  list = '['
  firstLine = True
  for row in History.List():
    if True == firstLine:
      firstLine = False
    else:
      list = list + ","
    list = list + \
      "{\"file\":\"" + os.path.basename(row[0]) + "\"," + \
      "\"user\":\"" + row[1] + "\"," + \
      "\"comment\":\"" + row[2] + "\"," + \
      "\"time\":\"" + row[3] + "\"}"
  return list + "]"

@app.get("/insert")
def insert():
  fileId = request.query.get('fileId')
  visible = request.query.get('secret')
  if ("on"==visible):
    visible = False
  else:
    visible = True
  dirName, fileName = File.Get(fileId)
  if ("on" == request.query.get('pause')):
    Book.AddTop( \
      u"空予約", \
      request.query.user, \
      "", \
      True, \
      "00:00:00.00", \
      1, \
      True)
  Book.AddTop( \
    os.path.join(dirName,fileName), \
    request.query.user, \
    request.query.comment, \
    visible, \
    videoInfo.GetDuration(os.path.join(dirName,fileName)), \
    request.query.audioIndex, \
    False)
  redirect( \
    "/" + request.query.back + \
    "?user=" + request.query.user + \
    "&keyword=" + request.query.keyword + \
    "&page=" + request.query.page)

@app.get("/playlist")
def playlist():
  return template( \
    'playlist', \
    name = request.query.user)

@app.get("/resttime/json")
def resttime():
  lock.acquire()
  sec = 0
  try:
    if True is video.CheckPlaying():
      val = re.split('[:.]', duration)
      sec += int(val[0])*60*60
      sec += int(val[1])*60
      sec += int(val[2])
      sec -= video.Position()
  except:
    pass
  sec += Book.GetTotalReserveTime()
  lock.release()
  return "{\"resttime\": " + str(int(sec)) + "}"

@app.get("/playlist/json")
def playlist():
  list = '['
  firstLine = True
  for row in Book.List():
    if False == firstLine:
      list = list + ","
    firstLine = False
    list = list + "{\"id\":" + str(row[0]) + ","
    list = list + "\"user\":\"" + row[3] + "\","
    if 1 == row[5]:
      list = list + "\"song\":\"" + os.path.basename(row[2]) + "\","
    else:
      list = list + u"\"song\":\"非公開\","
    list = list + "\"comment\":\"" + row[4] + "\"}"
  return list + "]"

# Delete Bookmark
@app.get("/forget")
def forget():

  # [[[ 1. Delete Bookmark ]]]
  Favorite.Delete(request.query.user, request.query.idx)

  # [[[ 2. Redirect Favorite View ]]]
  redirect( \
    "/favorites?user=" + request.query.user)

@app.get("/delete")
def delete():
  Book.Delete(int(request.query.bookId))
  redirect( \
    "/playlist?user=" + request.query.user)

@app.get("/reserve")
def reserve():
  if None is Book.ReserveDetail(request.query.bookId):
    redirect( \
      "/playlist?user=" + request.query.user)
  else:
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
    videoInfo.GetDuration(os.path.join(dirName,fileName)), \
    request.query.audioIndex, \
    False)
  if ("on" == request.query.get('pause')):
    Book.AddLast( \
      u"空予約", \
      request.query.user, \
      "", \
      True, \
      "00:00:00.00", \
      1, \
      True)
  redirect( \
    "/" + request.query.back + \
    "?user=" + request.query.user + \
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
    1, \
    True)
  redirect( \
    "/search?user=" + request.query.user + \
    "&keyword=" + request.query.keyword)

@app.get("/preview")
def preview():
  dirName, fileName = File.Get(request.query.fileId)
  return static_file(fileName, root=dirName)

@app.get("/setwifipass")
def setwifipass():
  # [[[ 1. Wifi ]]]
  regexp = re.compile(r'^[\x20-\x7E]*$')
  if len(request.query.password) < 8 or None is regexp.search(request.query.password):
    network.SetPassword(None)
  else:
    network.SetPassword(request.query.password)
  # [[[ 2. AudioPort ]]]
  if 0 == request.query.port.find("0"):
    # < HDMI >
    video.SetCurrentAudioPort("HDMI")
  else:
    # < RCA >
    video.SetCurrentAudioPort("RCA")
  redirect("/")

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
def resetAll():
  Book.Reset()
  File.Delete()
  History.Reset()
  Favorite.Reset()
  redirect("/")

@app.get("/initHistory")
def resetHistory():
  History.Reset()
  redirect("/")

# [[[ 1. Initialize HDMI Signal Switcher ]]]
hdmi = HDMI.HDMI()
video = Video.Video()
videoInfo = VideoInfo.VideoInfo()
network = Network.Network()
system = System.System()
vol = video.GetDefaultVolume()

# [[[ 2. Make QR-Code ]]]
img = qrcode.make("http://" + network.GetIP() + ":50000/")
img.save("static/url.png")
if len(network.GetPassword()) < 1:
  img = qrcode.make("WIFI:T:nopass;S:" + network.GetSSID() + ";P:;;")
else:
  img = qrcode.make("WIFI:T:WPA;S:" + network.GetSSID() + ";P:" + network.GetPassword() + ";;") 
img.save("static/ssid.png")

# [[[ 3. Refresh File List ]]]
File.init()

# [[[ 4. Start Browser ]]]
system.StartBrowser()

# [[[ 5. Start Web Server ]]]
web.serve(app,host="0.0.0.0",port=50000)

