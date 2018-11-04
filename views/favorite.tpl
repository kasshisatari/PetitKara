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

  <div role="main" class="ui-content">
% import File
% list = File.Detail(id,name)
{{!list}}
  </div>

  <div data-role="footer">
    <div data-role="navbar">
      <ul>
        <li><a href="#add" data-rel="dialog">予約</a></li>    
        <li><a href="#insertcheck" data-rel="dialog">割り込み予約</a></li>    
        <li><a href="#delete" data-rel="dialog">削除</a></li>    
      </ul>
    </div>
  </div>

</div>

<div id="delete" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
削除しますか。
    <form method="GET" action="forget" data-ajax="false">
      <input id="user" name="user" type="hidden" value="{{!name}}" />
      <input id="idx" name="idx" type="hidden" value="{{!idx}}" />
      <input type="submit" value="はい" />
      <a data-role="button" href="/" data-rel="back">いいえ</a>
    </form>
  </div>
  <div data-role="footer"></div>
</div>

<div id="add" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
予約しますか。
    <form method="GET" action="add" data-ajax="false">
      <input id="comment" name="comment" value="" type="text" />
      <input id="user" name="user" type="hidden" value="{{!name}}" />
      <input id="fileId" name="fileId" type="hidden" value="{{!id}}" />
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
      <input id="fileId" name="fileId" type="hidden" value="{{!id}}" />
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
