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
    <a href="config" data-role="button" rel="external">設定</a>
    <a href="#shutdown" data-role="button" data-rel="dialog">シャットダウン</a>
    <a href="#restart" data-role="button" data-rel="dialog">再起動</a>
    <a href="#reset" data-role="button" data-rel="dialog">リセット</a>
    <a href="#attention" data-role="button" data-rel="dialog">注意事項</a>
    <img src="../static/toppage.png">
    <br>
    SSID:{{!ssid}}
    <br>
    PASS:{{!password}}
    </div>
    <div data-role="footer">
      Version 1.3.27
    </div>
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
        <a data-role="button" href="#" rel="external" id="shutdown-target">はい</a>
	<a data-role="button" href="/" data-rel="back">いいえ</a>
        <script>
          $('#shutdown-target').click(function() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "shutdown");
            xhr.send();
            window.open('/', '_self').close();
            return false;
          });
        </script>
      </form>
    </div>
    <div data-role="footer"></div>
  </div>

  <div data-role="page" id="restart">
    <div data-role="header"><h1>確認</h1></div>
    <div data-role="content">
再起動します。よろしいでしょうか。
      <form>
        <a data-role="button" href="#" rel="external" id="restart-target">はい</a>
	<a data-role="button" href="/" data-rel="back">いいえ</a>
        <script>
          $('#restart-target').click(function() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "restart");
            xhr.send();
            window.open('/', '_self').close();
            return false;
          });
        </script>
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

  <div data-role="page" id="attention">
    <div data-role="header"><h1>注意事項</h1></div>
    <div data-role="content">
	    カラオケ店等にてコンセントを繋いで電源を使用する場合、店側の許可を得てください。刑法245条に抵触する『電気窃盗罪』が成立します。<br><br>
	    再生する動画像は営利目的への利用、インターネットに公開する、公衆の場での利用等、著作権法第38条第1項に抵触する場合、権利者の許諾を得てください。<br><br>
	    PetitKaraはMIT Licenseです。 以下に定める条件に従い、本ソフトウェアおよび関連文書のファイル（以下「ソフトウェア」）の複製を取得するすべての人に対し、ソフトウェアを無制限に扱うことを無償で許可します。これには、ソフトウェアの複製を使用、複写、変更、結合、掲載、頒布、サブライセンス、および/または販売する権利、およびソフトウェアを提供する相手に同じことを許可する権利も無制限に含まれます。<br><br>

上記の著作権表示および本許諾表示を、ソフトウェアのすべての複製または重要な部分に記載するものとします。<br><br>

ソフトウェアは「現状のまま」で、明示であるか暗黙であるかを問わず、何らの保証もなく提供されます。ここでいう保証とは、商品性、特定の目的への適合性、および権利非侵害についての保証も含みますが、それに限定されるものではありません。 作者または著作権者は、契約行為、不法行為、またはそれ以外であろうと、ソフトウェアに起因または関連し、あるいはソフトウェアの使用またはその他の扱いによって生じる一切の請求、損害、その他の義務について何らの責任も負わないものとします。
    </div>
    <div data-role="footer"></div>
  </div>

<script>
var xhr = new XMLHttpRequest();
var day = new Date();
xhr.open("GET", "sync?time=" + 
  day.getFullYear() + "/" + 
  day.getMonth()+1 + "/" + 
  day.getDate() + " " + 
  day.getHours() + ":" + 
  day.getMinutes() + ":" + 
  day.getSeconds());
xhr.send();
</script>

</body>
</html>

