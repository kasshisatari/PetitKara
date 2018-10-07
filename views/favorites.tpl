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
    <a href="search?user={{!name}}" rel="external">戻る</a>
    <h1>お気に入り</h1>
    <a href="current?user={{!name}}&back=favorite" rel="external">状態</a>
  </div>

  <div role="main" class="ui-content">
    <form class="ui-filterable">
      <input id="filterBasic-input" data-type="search">
    </form>
    <ul data-role="listview" data-filter="true" data-input="#filterBasic-input">
% import Favorite
% list = Favorite.FavoriteList(name)
{{!list}}
    </ul>
  </div>
  <div data-role="footer">
  </div>

</div>

</body>
</html>

