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

<div id="config" data-role="page">
  <div data-role="header">
    <a href="/" rel="external">戻る</a>
    <h1>設定</h1>
  </div>
  <div role="main" class="ui-content">
    <form method="GET" action="setwifipass" data-ajax="false">
      <label for="password">Wifiパスワード<br>8文字未満はパスワード無効<br>要再起動</label>
      <input id="password" name="password" type="text" value="{{!password}}" maxlength="63" />
      {{!rca}}
      <input type="submit" value="変更" />
    </form>
  </div>
  <div data-role="footer">
  </div>
</div>

</body>
</html>

