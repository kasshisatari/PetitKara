/*
Copyright 2018-2019 oscillo

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software 
and associated documentation files (the "Software"),
to deal in the Software without restriction, 
including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission 
notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

var fileSystem = new ActiveXObject("Scripting.FileSystemObject");

// [[[ 1. Python ]]]
if (!fileSystem.FileExists("python-3.7.3.exe"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://www.python.org/ftp/python/3.7.3/python-3.7.3.exe", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("python-3.7.3.exe", 2);
  stream.Close();
  stream = null;
  http = null;
}

// [[[ 2. VLC ]]]
if (!fileSystem.FileExists("vlc-3.0.6-win32.exe"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://vlc.letterboxdelivery.org/vlc/3.0.6/win32/vlc-3.0.6-win32.exe", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("vlc-3.0.6-win32.exe", 2);
  stream.Close();
  stream = null;
  http = null;
}

// [[[ 3. FFmpeg ]]]
if (!fileSystem.FileExists("ffmpeg-20190420-3a07aec-win32-static.zip"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-20190420-3a07aec-win32-static.zip", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("ffmpeg-20190420-3a07aec-win32-static.zip", 2);
  stream.Close();
  stream = null;
  http = null;
}

var shell = new ActiveXObject("Shell.Application");
var path = shell.NameSpace(fileSystem.GetFile(WScript.ScriptFullName).ParentFolder.Path);
var file = shell.NameSpace(fileSystem.GetFile(WScript.ScriptFullName).ParentFolder.Path + "\\ffmpeg-20190420-3a07aec-win32-static.zip");
path.CopyHere(file.items());

// [[[ 4. six ]]]
if (!fileSystem.FileExists("six-1.12.0-py2.py3-none-any.whl"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://files.pythonhosted.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("six-1.12.0-py2.py3-none-any.whl", 2);
  stream.Close();
  stream = null;
  http = null;
}

// [[[ 5. Image ]]]
if (!fileSystem.FileExists("image-1.5.27-py2.py3-none-any.whl"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://files.pythonhosted.org/packages/0c/ec/51969468a8b87f631cc0e60a6bf1e5f6eec8ef3fd2ee45dc760d5a93b82a/image-1.5.27-py2.py3-none-any.whl", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("image-1.5.27-py2.py3-none-any.whl", 2);
  stream.Close();
  stream = null;
  http = null;
}

// [[[ 6. Pillow ]]]
if (!fileSystem.FileExists("Pillow-6.0.0-cp37-cp37m-win32.whl"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://files.pythonhosted.org/packages/70/21/04723e78916eff8e09901dbb7dc9705f4de8a0dfe7882a9ed56982bd128e/Pillow-6.0.0-cp37-cp37m-win32.whl", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("Pillow-6.0.0-cp37-cp37m-win32.whl", 2);
  stream.Close();
  stream = null;
  http = null;
}

// [[[ 7. Django ]]]
if (!fileSystem.FileExists("Django-2.2-py3-none-any.whl"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://files.pythonhosted.org/packages/54/85/0bef63668fb170888c1a2970ec897d4528d6072f32dee27653381a332642/Django-2.2-py3-none-any.whl", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("Django-2.2-py3-none-any.whl", 2);
  stream.Close();
  stream = null;
  http = null;
}

// [[[ 8. pytz ]]]
if (!fileSystem.FileExists("pytz-2019.1-py2.py3-none-any.whl"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://files.pythonhosted.org/packages/3d/73/fe30c2daaaa0713420d0382b16fbb761409f532c56bdcc514bf7b6262bb6/pytz-2019.1-py2.py3-none-any.whl", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("pytz-2019.1-py2.py3-none-any.whl", 2);
  stream.Close();
  stream = null;
  http = null;
}

// [[[ 9. sqlparse ]]]
if (!fileSystem.FileExists("sqlparse-0.3.0-py2.py3-none-any.whl"))
{
  var http = new ActiveXObject("Microsoft.XMLHTTP");
  var stream = new ActiveXObject("ADODB.Stream");
  http.open("GET", "https://files.pythonhosted.org/packages/ef/53/900f7d2a54557c6a37886585a91336520e5539e3ae2423ff1102daf4f3a7/sqlparse-0.3.0-py2.py3-none-any.whl", false);
  http.send();
  stream.Type = 1;
  stream.Open();
  stream.Write(http.responseBody);
  stream.SaveToFile("sqlparse-0.3.0-py2.py3-none-any.whl", 2);
  stream.Close();
  stream = null;
  http = null;
}
