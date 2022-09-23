## 声明
 原作者：@qazwsxe11(www.t00ls.com)
 
 原文章：[【好人py交易器】](https://www.t00ls.com/viewthread.php?tid=67202&extra=&page=1)
 
 修改：修改为命令行形式，移除原工具UI相关内容，降低使用前置条件
 
 ````
 usage: GPoc.py [-h] [-c CHECKER] [-s STATUS] [-p PROXY] request

 positional arguments:
   request               请求数据包文件

 optional arguments:
   -h, --help            show this help message and exit
   -c CHECKER, --checker CHECKER
                        成功时响应包含的关键字(英文区分大小写)，例如：上传成功
   -s STATUS, --status STATUS
                        成功时响应码，例如：200
   -p PROXY, --proxy PROXY
                        设置poc使用的proxy, 例如：127.0.0.1:8080
 
 例如：python .\GPoc.py .\test.txt -s 204 -c ok -p "127.0.0.1:8080"
 ````
 
 
 
By T00ls.Net
