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
      records[i].song + 
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
</html>

