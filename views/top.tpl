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
    <div data-role="header"></div>
    <div role="main" class="ui-content">
      <form method="GET" action="search" data-ajax="false">
        <div class="ui-field-contain">
          <label for="user">名前：</label>
          <input id="user" name="user" type="text" data-clear-btn="true" data-clear-btn-text="クリア" />
        </div>
        <input id="keyword" name="keyword" type="hidden" value="" />
        <input type="submit" value="ログイン" />
      </form>
    <a href="#initHistory" data-role="button" data-rel="dialog">履歴初期化</a>
    <a href="#refresh" data-role="button" data-rel="dialog">曲情報更新</a>
    <a href="#shutdown" data-role="button" data-rel="dialog">シャットダウン</a>
    <a href="#restart" data-role="button" data-rel="dialog">再起動</a>
    <a href="#reset" data-role="button" data-rel="dialog">リセット</a>
    <img src="../static/toppage.png">
    </div>
    <div data-role="footer">Version 1.3.2</div>
  </div>

  <div data-role="page" id="refresh">
    <div data-role="header"><h1>確認</h1></div>
    <div data-role="content">
リストを取り込みます。しばらく時間がかかる場合があります。よろしいでしょうか。
      <form>
        <a data-role="button" href="refresh" rel="external">はい</a>
	<a data-role="button" href="/" data-rel="back">いいえ</a>
      </form>
    </div>
    <div data-role="footer"></div>
  </div>

  <div data-role="page" id="initHistory">
    <div data-role="header"><h1>確認</h1></div>
    <div data-role="content">
履歴を初期化します。よろしいでしょうか。
      <form>
        <a data-role="button" href="initHistory" rel="external">はい</a>
	<a data-role="button" href="/" data-rel="back">いいえ</a>
      </form>
    </div>
    <div data-role="footer"></div>
  </div>

  <div data-role="page" id="shutdown">
    <div data-role="header"><h1>確認</h1></div>
    <div data-role="content">
シャットダウンします。よろしいでしょうか。
      <form>
        <a data-role="button" href="shutdown" rel="external">はい</a>
	<a data-role="button" href="/" data-rel="back">いいえ</a>
      </form>
    </div>
    <div data-role="footer"></div>
  </div>

  <div data-role="page" id="restart">
    <div data-role="header"><h1>確認</h1></div>
    <div data-role="content">
再起動します。よろしいでしょうか。
      <form>
        <a data-role="button" href="restart" rel="external">はい</a>
	<a data-role="button" href="/" data-rel="back">いいえ</a>
      </form>
    </div>
    <div data-role="footer"></div>
  </div>

  <div data-role="page" id="reset">
    <div data-role="header"><h1>確認</h1></div>
    <div data-role="content">
曲情報、履歴、予約の全てを初期化します。よろしいでしょうか。
      <form>
        <a data-role="button" href="reset" rel="external">はい</a>
	<a data-role="button" href="/" data-rel="back">いいえ</a>
      </form>
    </div>
    <div data-role="footer"></div>
  </div>

</body>
</html>

