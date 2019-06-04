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

<div id="search" data-role="page">
  <div data-role="header">
    <a href="/" rel="external">ログアウト</a>
    <h1>{{!name}}</h1>
    <a href="current?user={{!name}}&back=search" rel="external">状態</a>
  </div>
  <div role="main" class="ui-content">
    <form method="GET" action="list?user={{!name}}">
      <div class="ui-field-contain">
        <label for="keyword">キーワード：</label>
	<input id="keyword" name="keyword" type="text" data-clear-btn="true" data-clear-btn-text="クリア" value="{{!keyword}}" />
	<input id="page" name="page" type="hidden" value="1" />
      </div>
      <input type="submit" value="検索" />
    </form>
    <a href="#dummy" data-role="button" data-rel="dialog">空予約</a>
  </div>
  <div data-role="footer">
    <div data-role="navbar">
      <ul>
        <li><a href="playlist?user={{!name}}" rel="external">予約一覧</a></li>
        <li><a href="history?user={{!name}}" rel="external">履歴一覧</a></li>
        <li><a href="favorites?user={{!name}}" rel="external">お気に入り一覧</a></li>
      </ul>
    </div>
  </div>
</div>

<div id="dummy" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
空予約しますか。空予約すると、再開するには状態画面から「再開」を選択する必要があります。
    <form>
    <a data-role="button" href="dummy?user={{!name}}&keyword={{!keyword}}" rel="external">はい</a>
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

