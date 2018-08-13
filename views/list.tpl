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
% import File 
% count = File.Count(keyword)
<a href="search?user={{!name}}&keyword={{!keyword}}" rel="external">戻る</a>
    <h1>{{!keyword}} {{!page}}ページ目  {{!count}}件</h1>
    <a href="/" rel="external">ログアウト</a>
  </div>

  <div role="main" class="ui-content">
    <ul data-role="listview">
% list = File.Search(keyword,name,page)
% end
{{!list}}
    </ul>
  </div>
  <div data-role="footer">
% page = File.Page(keyword,name)
{{!page}}
  </div>

</div>

</body>
</html>

