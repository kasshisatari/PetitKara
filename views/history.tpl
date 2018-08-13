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
% import History
    <a href="search?user={{!name}}" rel="external">戻る</a>
    <h1>履歴</h1>
    <a href="/" rel="external">ログアウト</a>
  </div>

  <div role="main" class="ui-content">
    <ul data-role="listview">
% list = History.Historylist()
% end
{{!list}}
    </ul>
  </div>
  <div data-role="footer">
  </div>

</div>

</body>
</html>

