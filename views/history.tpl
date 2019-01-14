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
    <h1>履歴</h1>
    <a href="current?user={{!name}}&back=history" rel="external">状態</a>
  </div>

  <div role="main" class="ui-content">
    <ul data-role="listview" id="list">
    </ul>
  </div>
  <div data-role="footer">
  </div>

</div>
<script>
var reqListener = function()
{
  $('#list').empty();
  var records = $.parseJSON(this.responseText);
  for (i in records)
  {
    $('#list').append(
      '<li style=\"white-space:pre-line;\">' +
      '<a href=\"historydetail?user={{!name}}&time=' + records[i].time + '\" rel=\"external\">' +
      records[i].user + '<br>' +
      records[i].file + '<br>' +
      records[i].comment +
      '</a>' +
      '</li>');
    $('#list').listview("refresh");
  }
}
var reload = function()
{
  var xhr = new XMLHttpRequest();
  xhr.addEventListener("load", reqListener);
  xhr.open("GET", "history/json");
  xhr.send();
}
reload();
setInterval(reload, 5000);
</script>
</body>
</html>

