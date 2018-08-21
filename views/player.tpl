<html>
<head>
<meta http-equiv="Refresh" content="3">
</head>
<body>
<table border="1">
% import Book
% import os
% list = ''
% for row in Book.List():
%   list = list +  \
%     "<tr><td>" + row[3] + "</td>" + \
%     "<td>" + row[4] + "</td>" + \
%     "<td>" + os.path.basename(row[2]) + "</td></tr>"
% end
{{!list}}
</table>
<br>
<img src="static/toppage.png">
</body>
</html>
