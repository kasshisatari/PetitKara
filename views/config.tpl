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

<div id="config" data-role="page">
  <div data-role="header">
    <a href="/" rel="external">戻る</a>
    <h1>設定</h1>
  </div>
  <div role="main" class="ui-content">
    <form method="GET" action="setwifipass" data-ajax="false">
      <label for="password">Wifiパスワード<br>8文字未満はパスワード無効<br>要再起動</label>
      <input id="password" name="password" type="text" value="{{!password}}" maxlength="63" />
      {{!rca}}
      {{!wifi}}
      <input type="submit" value="変更" />
    </form>
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
  closeAlert(json.user+"さんが"+json.song+"を予約しました。",3000);
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

