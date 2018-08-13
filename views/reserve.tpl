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
  </div>

  <div role="main" class="ui-content">
% import Book
% list = Book.ReserveDetail(id)
{{!list}}
  </div>

  <div data-role="footer">
    <div data-role="navbar">
      <ul>
        <li><a href="#deleteCheck" data-rel="dialog">削除</a></li>
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
</html>

