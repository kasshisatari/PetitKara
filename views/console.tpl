<html>
<head>
<script src="static/jquery-1.11.1.min.js"></script>
</head>
<body>
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

var reload = function()
{
  var xhr = new XMLHttpRequest();
  xhr.addEventListener("load", reqListener);
  xhr.open("GET", "playlist/json");
  xhr.send();
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
<br>
<img src="static/toppage.png">
<br>
{{!ssid}}
</body>
</html>
