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
  動画が見つかりません。<br>
  曲情報を更新してください。
  </div>

  <div data-role="footer">
    <div data-role="navbar">
    </div>
  </div>

</div>

</body>
</html>

