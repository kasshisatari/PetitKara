<html>
<head>
<script src="static/jquery-1.11.1.min.js"></script>
<title>PetitKara</title>
</head>
<body>
<p id="pause"></p>
<table border="1" id="list">
</table>
<script>
var reqListener = function()
{
  $('#list').empty();
  var records = $.parseJSON(this.responseText);
  for (i in records)
  {
    $('#list').append(
      '<tr>' + 
      '<td bgcolor="cornflower"><font size="6">' + records[i].user + '</font></td>' +
      '<td bgcolor="linen"><font size="6">' + records[i].song + '</font></td>' +
      '<td bgcolor="mistyrose"><font size="6">' + records[i].comment + '</font></td>' + 
      '</tr>');
  }
}

var pauseListener = function()
{
  var json = $.parseJSON(this.responseText);
  if (true == json.playing)
  {
    $("#pause").text("一時停止中");
  }
  else
  {
    $("#pause").text("");
  }
}

var reload = function()
{
  var playlist = new XMLHttpRequest();
  playlist.addEventListener("load", reqListener);
  playlist.open("GET", "playlist/json");
  playlist.send();
  var pause = new XMLHttpRequest();
  pause.addEventListener("load", pauseListener);
  pause.open("GET", "playing/json");
  pause.send();
}

var playVideo = function()
{
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "play");
  xhr.send();
}

setInterval(reload, 1000);
setInterval(playVideo, 5000);

</script>
<table width="100%">
<td>
<font size="6">
First, connect the following Wi-Fi.
<br>
SSID:{{!ssid}}
</font>
<br>
<font size="6">
PASS:{{!password}}
</font>
<br>
<img src="static/ssid.png">
</td>
<td align="right">
<font size="6">
Second, go to the following URL.
<br>
http://{{!ip}}:50000/
</font>
<br>
<img src="static/url.png">
</td>
</table>
</body>

</html>
