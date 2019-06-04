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
    <a href="playlist?user={{!name}}" rel="external">戻る</a>
    <h1>予約詳細</h1>
    <a href="current?user={{!name}}&back=reserve&bookId={{!id}}" rel="external">状態</a>
  </div>

  <div role="main" class="ui-content">
% import Book
% list = Book.ReserveDetail(id)
{{!list}}
  </div>

  <div data-role="footer">
    <div data-role="navbar">
      <ul>
        <li><a href="moveup?user={{!name}}&bookId={{!id}}" rel="external">上に移動</a></li>
        <li><a href="#deleteCheck" data-rel="dialog">削除</a></li>
        <li><a href="movedown?user={{!name}}&bookId={{!id}}" rel="external">下に移動</a></li>
      </ul>
    </div>
  </div>
</div>

<div id="deleteCheck" data-role="page">
  <div data-role="header"><h1>確認</h1></div>

  <div data-role="content">
動画予約を削除しますか。
    <form>
      <a data-role="button" href="delete?user={{!name}}&bookId={{!id}}" rel="external">はい</a>
      <a data-role="button" href="/" data-rel="back">いいえ</a>
    </form>
  </div>

  <div data-role="footer"></div>
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

