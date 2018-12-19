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
    <h1>{{!name}}</h1>
  </div>
  <div role="main" class="ui-content">
再生中の動画はありません。<br>
<p id="vol">音量は{{!vol}}dBです。</p><br>
  </div>
  <div data-role="footer">
    <a href="#" id="button-down">音量小</a>
    <a href="#" id="button-up">音量大</a>
    <a href="pause?user={{!name}}&back={{!back}}&keyword={{!keyword}}&page={{!page}}&fileId={{!fileId}}&bookId={{!bookId}}&idx={{!idx}}" rel="external">{{!pause}}</a>
<script>
  var volFunc = function()
  {
    var json = $.parseJSON(this.responseText);
    $('#vol').text("音量は" + String(json.vol) + "dBです。");
  }
  $('#button-down').click(function(){
    var xhr=new XMLHttpRequest();
    xhr.addEventListener("load", volFunc);
    xhr.open("GET","down");
    xhr.send();
  });
  $('#button-up').click(function(){
    var xhr=new XMLHttpRequest();
    xhr.addEventListener("load", volFunc);
    xhr.open("GET","up");
    xhr.send();
  });

</script>
  </div>
</div>

</body>
</html>

