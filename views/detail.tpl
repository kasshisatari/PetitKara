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
  <a href="list?user={{!name}}&keyword={{!keyword}}&page={{!page}}" rel="external">戻る</a>
    <h1>{{!name}}</h1>
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
      </ul>
    </div>
  </div>

</div>

<div id="add" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
予約しますか。
    <form>
    <a data-role="button" href="add?user={{!name}}&fileId={{!id}}&keyword={{!keyword}}&page={{!page}}" rel="external">はい</a>
    <a data-role="button" href="/" data-rel="back">いいえ</a>
    </form>
  </div>
  <div data-role="footer"></div>
</div>

<div id="insertcheck" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
割り込み予約しますか。
    <form>
      <a data-role="button" href="insert?user={{!name}}&fileId={{!id}}&keyword={{!keyword}}&page={{!page}}" rel="external">はい</a>
      <a data-role="button" href="/" data-rel="back">いいえ</a>
    </form>
  </div>
  <div data-role="footer"></div>
</div>

</body>
</html>

