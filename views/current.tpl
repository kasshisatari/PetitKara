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

<div data-role="page">
  <div data-role="header" data-add-back-btn="true">
    <a href="search?user={{!name}}" rel="external">戻る</a>
    <h1>{{!user}}</h1>
  </div>
  <div role="main" class="ui-content">
{{!path}}<br>
% import VideoInfo
% duration = VideoInfo.GetDuration(path)
{{!duration}}<br>
音量は{{!vol}}dBです。
  </div>
  <div data-role="footer">
    <a href="down?user={{!name}}" rel="external">音量小</a>
    <a href="up?user={{!name}}" rel="external">音量大</a>
    <a href="rew?user={{!name}}" rel="external">巻き戻し</a>
    <a href="ff?user={{!name}}" rel="external">早送り</a>
    <a href="audio?user={{!name}}" rel="external">音声切り替え</a>
    <a href="pause?user={{!name}}" rel="external">一時停止</a>
    <a href="#confirm" data-rel="dialog">中止</a>
  </div>
</div>

<div id="confirm" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
動画再生を終了しますか。
  <form>
  <a data-role="button" href="stop?user={{!name}}" rel="external">はい</a>
  <a data-role="button" href="/" data-rel="back">いいえ</a>
  </form>
  </div>
  <div data-role="footer"></div>
</div>

</body>
</html>

