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
  <a href="favorites?user={{!name}}" rel="external">戻る</a>
    <h1>{{!name}}</h1>
    <a href="current?user={{!name}}&back=favorite&idx={{!idx}}" rel="external">状態</a>
  </div>
    動画が見つかりません。<br>
    曲情報を更新してください。
  <div role="main" class="ui-content">

  </div>

  <div data-role="footer">
    <div data-role="navbar">
    </div>
  </div>

</div>

<div id="add" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
予約しますか。
    <form method="GET" action="add" data-ajax="false">
      <input id="comment" name="comment" value="" type="text" />
      <input id="user" name="user" type="hidden" value="{{!name}}" />
      <input id="back" name="back" type="hidden" value="favorites" />
      <label>
        <input id="secret" name="secret" type="checkbox" />非公開
      </label>
      <input type="submit" value="はい" />
      <a data-role="button" href="/" data-rel="back">いいえ</a>
    </form>
  </div>
  <div data-role="footer"></div>
</div>

<div id="insertcheck" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
割り込み予約しますか。
    <form method="GET" action="insert" data-ajax="false">
      <input id="comment" name="comment" value="" type="text" />
      <input id="user" name="user" type="hidden" value="{{!name}}" />
      <input id="back" name="back" type="hidden" value="favorites" />
      <label>
        <input id="secret" name="secret" type="checkbox" />非公開
      </label>
      <input type="submit" value="はい" />
      <a data-role="button" href="/" data-rel="back">いいえ</a>
    </form>
  </div>
  <div data-role="footer"></div>
</div>

</body>
</html>

