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
音量は{{!vol}}dBです。<br>
  </div>
  <div data-role="footer">
    <a href="down?user={{!name}}&back={{!back}}&keyword={{!keyword}}&page={{!page}}&fileId={{!fileId}}&bookId={{!bookId}}&idx={{!idx}}" rel="external">音量小</a>
    <a href="up?user={{!name}}&back={{!back}}&keyword={{!keyword}}&page={{!page}}&fileId={{!fileId}}&bookId={{!bookId}}&idx={{!idx}}" rel="external">音量大</a>
    <a href="pause?user={{!name}}&back={{!back}}&keyword={{!keyword}}&page={{!page}}&fileId={{!fileId}}&bookId={{!bookId}}&idx={{!idx}}" rel="external">{{!pause}}</a>
  </div>
</div>

</body>
</html>

