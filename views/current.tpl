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
    <a href="{{!back}}?user={{!name}}&keyword={{!keyword}}&page={{!page}}&fileId={{!fileId}}&bookId={{!bookId}}&idx={{!idx}}" rel="external">戻る</a>
    <h1 id="text-user"></h1>
  </div>
  <div role="main" class="ui-content">
    <p id="path"></p>
    <p id="duration"></p>
    <p id="vol"></p>
  </div>
  <div data-role="footer">
    <a href="#" id="button-down">音量小</a>
    <a href="#" id="button-up">音量大</a>
    <a href="#" id="button-rew">巻き戻し</a>
    <a href="#" id="button-ff">早送り</a>
    <a href="#" id="button-audio">音声切り替え</a>
    <a href="#" id="button-pause"></a>
    <a href="#confirm" id="button-stop" data-rel="dialog">中止</a>
<script>
  var volFunc = function()
  {
    var json = $.parseJSON(this.responseText);
    $('#vol').text("音量は" + String(json.vol) + "dBです。");
  }
  var infoFunc = function()
  {
    var json = $.parseJSON(this.responseText);
    if (true == json.play)
    {
      $('#path').text(json.path);
      $('#duration').text(json.duration);
      $('#text-user').text(json.user);
      $('#button-rew').show();
      $('#button-ff').show();
      $('#button-audio').show();
      $('#button-stop').show();
    }
    else
    {
      $('#path').text("再生中の動画はありません。");
      $('#duration').text("");
      $('#text-user').text("");
      $('#button-rew').hide();
      $('#button-ff').hide();
      $('#button-audio').hide();
      $('#button-stop').hide();
    }
    $('#vol').text("音量は" + String(json.vol) + "dBです。");
    if (true == json.pause)
    {
      $('#button-pause').text("再開");
    }
    else
    {
      $('#button-pause').text("一時停止");
    }
  }
  var statusFunc = function()
  {
    var json = $.parseJSON(this.responseText);
    if (true == json.playing)
    {
      $('#button-pause').text("再開");
    }
    else
    {
      $('#button-pause').text("一時停止");
    }
  }
  var loadFunc = function()
  {
    var xhrVol = new XMLHttpRequest();
    xhrVol.addEventListener("load", infoFunc);
    xhrVol.open("GET", "current/json");
    xhrVol.send();
  }
  $(function(){
    loadFunc();
    setInterval(loadFunc, 1000);
  });
  $('#button-down').click(function(){
    var xhr=new XMLHttpRequest();
    xhr.addEventListener("load", volFunc);
    xhr.open("GET","vol/json?step=-300");
    xhr.send();
  });
  $('#button-up').click(function(){
    var xhr=new XMLHttpRequest();
    xhr.addEventListener("load", volFunc);
    xhr.open("GET","vol/json?step=300");
    xhr.send();
  });
  $('#button-pause').click(function() {
    var xhr=new XMLHttpRequest();
    xhr.addEventListener("load", statusFunc);
    xhr.open("GET", "pause/json");
    xhr.send();
  });
  $('#button-rew').click(function() {
    var xhr=new XMLHttpRequest();
    xhr.open("GET", "pos?offset=-5000");
    xhr.send();
  });
  $('#button-ff').click(function() {
    var xhr=new XMLHttpRequest();
    xhr.open("GET", "pos?offset=5000");
    xhr.send();
  });
  $('#button-audio').click(function() {
    var xhr=new XMLHttpRequest();
    xhr.open("GET", "audio");
    xhr.send();
  });
</script>
  </div>
</div>

<div id="confirm" data-role="page">
  <div data-role="header"><h1>確認</h1></div>
  <div data-role="content">
動画再生を終了しますか。
  <form>
  <a data-role="button" href="stop?user={{!name}}&keyword={{!keyword}}&back={{!back}}&page={{!page}}&fileId={{!fileId}}&bookId={{!bookId}}&idx={{!idx}}" rel="external">はい</a>
  <a data-role="button" href="/" data-rel="back">いいえ</a>
  </form>
  </div>
  <div data-role="footer"></div>
</div>

</body>
</html>

