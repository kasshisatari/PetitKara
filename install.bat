REM Copyright 2018-2019 oscillo
REM
REM Permission is hereby granted, free of charge,
REM to any person obtaining a copy of this software 
REM and associated documentation files (the "Software"),
REM to deal in the Software without restriction, 
REM including without limitation the rights to use,
REM copy, modify, merge, publish, distribute, sublicense,
REM and/or sell copies of the Software, and to permit
REM persons to whom the Software is furnished to do so,
REM subject to the following conditions:
REM
REM The above copyright notice and this permission 
REM notice shall be included in all copies or substantial
REM portions of the Software.
REM 
REM THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
REM OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
REM LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
REM FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
REM IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
REM LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
REM WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
REM ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
REM OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

cscript //nologo Win\download.js
Win\python-3.7.3.exe /quiet
%localappdata%\Programs\Python\Python37-32\python.exe -m pip install Win\six-1.12.0-py2.py3-none-any.whl
%localappdata%\Programs\Python\Python37-32\python.exe -m pip install Win\sqlparse-0.3.0-py2.py3-none-any.whl
%localappdata%\Programs\Python\Python37-32\python.exe -m pip install Win\pytz-2019.1-py2.py3-none-any.whl
%localappdata%\Programs\Python\Python37-32\python.exe -m pip install Win\Django-2.2-py3-none-any.whl
%localappdata%\Programs\Python\Python37-32\python.exe -m pip install Win\Pillow-6.0.0-cp37-cp37m-win32.whl 
%localappdata%\Programs\Python\Python37-32\python.exe -m pip install Win\image-1.5.27-py2.py3-none-any.whl
Win\vlc-3.0.6-win32.exe /L=1041 /S
copy Win\ffmpeg-latest-win32-static\bin\ffprobe.exe Win
