## 声明
 原作者：@qazwsxe11
 
 原文章：[【好人py交易器】](https://www.t00ls.com/viewthread.php?tid=67202&extra=&page=1)

### 版本描述 
 V2
 原版本针对任何请求数据均采用字符串格式处理，对文件上传、反序列化等场景可能导致payload异常。故V2版本新增支持二进制模式。
 另外，针对从burpsuite中使用"copy to file"保存的request换行符为\r\n的场景进行了处理。

 ````
 usage: GPoc_v2.py [-h] [-c CHECKER] [-s STATUS] [-p PROXY] [-m MODE] request

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
   -m MODE, --mode MODE  处理模式，’0‘代表以字符串格式处理、’1‘代表以二进制格式处理(默认为0)
 
 python .\GPoc_v2.py -c Created -s 201 -p 127.0.0.1:2345 -m 1 .\test2.bin
 ````
 
 V1
 修改：修改为命令行形式，移除原工具UI相关内容，降低使用前置条件。
 
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

@skydiver
By T00ls.Net