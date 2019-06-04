<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>PetitKara</title>
<link rel="stylesheet"
  href="static/jquery.mobile-1.4.5.min.css" />
<script src="static/jquery-1.11.1.min.js"></script>
<script language="JavaScript">
$(document).bind("mobileinit", function(){
$.mobile.pushStateEnabled = false;
});
</script>
<script src="static/jquery.mobile-1.4.5.min.js">
</script>
</head>
<body>
<div data-role="page" data-title="PetitKara">
  <div data-role="header">
  <a href="search?user={{!name}}" rel="external">戻る</a>
<script>
var restListener = function()
{
  var restTime = $.parseJSON(this.responseText).resttime;
  if (0 == restTime)
  {
    $("#finish").text("終了予定:--:--:--");
    $("#resttime").text("残時間:--:--:--");
  }
  else
  {
    var day = new Date();
    day.setSeconds(day.getSeconds() + restTime);
    $("#finish").text(
      "終了予定:" + 
      ("0" + day.getHours()).slice(-2) + ":" + 
      ("0" + day.getMinutes()).slice(-2) + ":" + 
      ("0" + day.getSeconds()).slice(-2));
    $("#resttime").text(
      "残時間:" + 
      ("0" + String(parseInt(restTime/60/60))).slice(-2) + ":" + 
      ("0" + String(parseInt((restTime/60)%60))).slice(-2) + ":" + 
      ("0" + String(parseInt(restTime%60))).slice(-2));
  }
}
var playlistListener = function()
{
  $('#list').empty();
  var records = $.parseJSON(this.responseText);
  for (i in records)
  {
    $('#list').append(
      "<li><a href=\"reserve?user=" + "{{!name}}" + 
      "&bookId=" + String(records[i].id) + 
      "\" rel=\"external\">" + 
      records[i].user + "<br>" + 
      records[i].song + "<br>" + 
      records[i].comment + 
      "</a></li>");
  }
  $('#list').listview('refresh');
}
var reload = function()
{
  var playlist = new XMLHttpRequest();
  playlist.addEventListener("load", playlistListener);
  playlist.open("GET", "playlist/json");
  playlist.send();
  var resttime = new XMLHttpRequest();
  resttime.addEventListener("load", restListener);
  resttime.open("GET", "resttime/json");
  resttime.send();
}
reload();
setInterval(reload, 1000);
</script>
    <h1>
      予約一覧<br>
      <p id="finish"></p>
      <p id="resttime"></p>
    </h1>
    <a href="current?user={{!name}}&back=playlist" rel="external">状態</a>
  </div>
  <div role="main" class="ui-content">
    <ul data-role="listview" id="list">
    </ul>
  </div>
  <div data-role="footer">
  </div>
</div>
</body>
<script>
var bookYear = 0;
var bookMonth = 0;
var bookDay = 0;
var bookHour = 0;
var bookMinute = 0;
var bookSecond = 0;
var bookFlag = false;
function closeAlert(msg,ms)
{
 var div = document.createElement("div");
 div.setAttribute(
   "style","position:fixed;top:10%;left:10%;right:10%;background-color:white;");
 div.innerHTML = msg;
 setTimeout(function(){
  div.parentNode.removeChild(div);
 },ms);
 document.body.appendChild(div);
}
var pushListener = function()
{
  var json = $.parseJSON(this.responseText);
  if (false == json.valid || false == bookFlag)
  {
    bookFlag = true;
    if (true == json.valid)
    {
      bookYear = json.year;
      bookMonth = json.month;
      bookDay = json.day;
      bookHour = json.hour;
      bookMinute = json.minute;
      bookSecond = json.second;
    }
    return;
  }
  if (
    bookYear == json.year &&
    bookMonth == json.month &&
    bookDay == json.day &&
    bookHour == json.hour &&
    bookMinute  == json.minute &&
    bookSecond == json.second)
  {
    return;
  }
  bookYear = json.year;
  bookMonth = json.month;
  bookDay = json.day;
  bookHour = json.hour;
  bookMinute = json.minute;
  bookSecond = json.second;
  if (true == json.visible)
  {
    closeAlert(json.user+"さんが"+json.song+"を予約しました。",3000);
  }
  else
  {
    closeAlert(json.user+"さんが予約しました。",3000);
  }
}
var pushFunc = function()
{
  var pushXhr = new XMLHttpRequest();
  pushXhr.addEventListener("load", pushListener);
  pushXhr.open("GET", "pushbook");
  pushXhr.send();
}
pushFunc();
setInterval(pushFunc, 1000);
</script>

</html>

