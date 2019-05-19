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
    <a href="{{!back}}?user={{!name}}&keyword={{!keyword}}&page={{!page}}&fileId={{!fileId}}&bookId={{!bookId}}&idx={{!idx}}&time={{!time}}" rel="external">戻る</a>
    <h1 id="text-user"></h1>
  </div>
  <div role="main" class="ui-content">
    <p id="path"></p>
    <p id="duration"></p>
    <progress id="posbar" value="0" max="0"></progress>
    <p id="vol"></p>
  </div>
  <div data-role="footer">
    <a href="#" id="button-down">音量小</a>
    <a href="#" id="button-up">音量大</a>
    <a href="#" id="button-rew">早戻し</a>
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
  var duration = "";
  var loadFlag = false;
  var playFlag = false;
  var posFunc = function()
  {
    var json = $.parseJSON(this.responseText);
    if (true == json.play)
    {
      hour = ('00' + String(Math.floor(json.pos / 3600))).slice(-2);
      min = ('00' + String(Math.floor((json.pos % 3600) / 60))).slice(-2);
      sec = ('00' + String(json.pos % 60)).slice(-2);
      $('#posbar').prop("value", json.pos);
      $('#posbar').prop("max", json.duration);
      $('#duration').text(hour + ":" + min + ":" + sec + "/" + duration);
      loadFlag = false;
      playFlag = true;
    }
    else
    {
      loadFlag = false;
      playFlag = false;
    }
  }
  var infoFunc = function()
  {
    var json = $.parseJSON(this.responseText);
    if (true == json.play)
    {
      hour = ('00' + String(Math.floor(json.pos / 3600))).slice(-2);
      min = ('00' + String(Math.floor((json.pos % 3600) / 60))).slice(-2);
      sec = ('00' + String(json.pos % 60)).slice(-2);
      duration = ('00' + String(Math.floor(json.duration / 3600))).slice(-2) + ":" +
        ('00' + String(Math.floor((json.duration % 3600) / 60))).slice(-2)+ ":" + 
        ('00' + String(json.duration % 60)).slice(-2);
      $('#posbar').prop("value", json.pos);
      $('#posbar').prop("max", json.duration);
      $('#path').text(json.path);
      $('#duration').text(hour + ":" + min + ":" + sec + "/" + duration);
      $('#text-user').text(json.user);
      $('#button-rew').show();
      $('#button-ff').show();
      $('#button-audio').show();
      $('#button-stop').show();
      loadFlag = true;
      playFlag = true;
    }
    else
    {
      $('#path').text("再生中の動画はありません。");
      $('#duration').text("");
      $('#posbar').prop("value", 0);
      $('#posbar').prop("max", 0);
      $('#text-user').text("");
      $('#button-rew').hide();
      $('#button-ff').hide();
      $('#button-audio').hide();
      $('#button-stop').hide();
      playFlag = false;
      loadFlag = true;
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
    if (false == loadFlag)
    {
      var xhr = new XMLHttpRequest();
      xhr.addEventListener("load", infoFunc);
      xhr.open("GET", "current/json");
      xhr.send();
    }
    else if (true == playFlag)
    {
      var xhr = new XMLHttpRequest();
      xhr.addEventListener("load", posFunc);
      xhr.open("GET", "pos/json");
      xhr.send();
    }
    else
    {
      loadFlag = false;
    }
  }
  $(function(){
    loadFunc();
    setInterval(loadFunc, 500);
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
  <a data-role="button" href="stop?user={{!name}}&keyword={{!keyword}}&back={{!back}}&page={{!page}}&fileId={{!fileId}}&bookId={{!bookId}}&idx={{!idx}}&time={{!time}}" rel="external">はい</a>
  <a data-role="button" href="/" data-rel="back">いいえ</a>
  </form>
  </div>
  <div data-role="footer"></div>
</div>

</body>
</html>

