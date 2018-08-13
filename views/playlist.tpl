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
% import Book
% time = Book.GetTotalReserveTime()
    <h1>
      予約一覧<br>
      {{!time}}
    </h1>
  </div>
  <div role="main" class="ui-content">
    <ul data-role="listview">
% list = Book.Playlist(name)
{{!list}}
    </ul>
  </div>
  <div data-role="footer">
  </div>
</div>
</body>
</html>

