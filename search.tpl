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
</html>

