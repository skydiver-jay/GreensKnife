# coding=utf-8
import argparse
import base64
import os
import time

"""
# 当前讲request作为文本处理，可能导致非字符串类的请求异常；
# 修改一个版本，以二进制形势处理。
"""
sp_0 = "\r\n".encode()
sp_1 = "\n".encode()
sp_2 = ":".encode()
sp_3 = "".encode()
sp_4 = '"'.encode()
sp_5 = '\\'.encode()
sp_6 = " ".encode()


# reqf为请求文件路径
# chk/st/prx，string类型的输入需要全部转为byte类型
def get_poc_binay(reqf, chk=None, st=None, prx=None):
    if chk is not None:
        chk = chk.encode()
    st = st.encode()
    if prx is not None:
        prx = prx.encode()

    with open(reqf, 'rb') as f0:
        content = f0.read()
        f0.seek(0)
        if sp_0 in f0.readline():
            line_break = sp_0
        else:
            line_break = sp_1
    f0.close()
    lb = line_break
    reqtxt = content

    c = 0
    body = "".encode()
    headers = {}
    for i in reqtxt.split(lb):
        if sp_2 in i and c == 0:
            key = i.split(sp_2)[0].strip()
            n = i.split(key + sp_2)[1].strip()
            if key == "Host".encode() or key == "Content-Length".encode():
                pass
            else:
                headers[key] = n

        if i == sp_3:
            c = 1
        if c == 1:
            body = body + i + lb

    body = base64.b64encode(body)

    # ff : http method, get/post/put...
    ff = reqtxt.split(lb)[0].split(sp_6)[0]
    ff = ff.lower()
    # print("method:", ff)

    path = reqtxt.split(lb)[0].split(sp_6)[1]
    # print("path:", path)

    # yz: 结果判定条件
    yz = '0'.encode()
    if st is not None and chk is not None:
        yz = 'h1.status_code=='.encode() + st + ' and "'.encode() + chk + '" in h1.text'.encode()
    elif st is not None:
        yz = 'h1.status_code=='.encode() + st
    elif chk is not None:
        yz = sp_4 + chk + '" in h1.text'.encode()

    dl = sp_3
    # dl : 代理
    if prx is not None:
        dl = prx

    with open('模板2.txt', 'rb') as f1:
        poc_text = f1.read()
    poc_text = poc_text.replace("$body".encode(), body). \
        replace("$ff".encode(), ff). \
        replace("$path".encode(), path). \
        replace("$headers".encode(), str(headers).encode()). \
        replace("$yz".encode(), yz).replace("$proxy".encode(), dl)
    if ff == "get".encode():
        poc_text = poc_text.replace(",data=data".encode(), sp_3).replace("data=\"\"".encode(), sp_3)
    if dl == sp_3:
        poc_text = poc_text.replace(",proxies=proxies".encode(), sp_3).replace(
            "proxies = {'http': 'http://'+proxy, 'https': 'http://'+proxy}".encode(), sp_3).replace("proxy=''".encode(),
                                                                                                    sp_3)

    poc_file_name = "poc_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".py"
    file = open('poc/' + poc_file_name, 'wb')

    file.write(poc_text)
    file.close()
    # cmd = 'start cmd /k "cd poc & python poc.py -h"'
    # os.system(cmd)


# reqf为请求文件路径
# chk/st/prx，为string类型的输入
def get_poc_normal(reqf, chk=None, st=None, prx=None):
    with open(reqf, 'r', encoding="utf-8") as f0:
        content = f0.read()
        f0.seek(0)
        if '\r\n' in f0.readline():
            line_break = '\r\n'
        else:
            line_break = '\n'
    f0.close()
    lb = line_break
    reqtxt = content

    c = 0
    body = ""
    headers = {}
    for i in reqtxt.split(lb):
        if ":" in i and c == 0:
            key = str(i).split(":")[0].strip()
            n = str(i).split(key + ":")[1].strip()
            if key == "Host" or key == "Content-Length":
                pass
            else:
                headers[key] = n

        if i == "":
            c = 1
        if c == 1:
            body = body + i

    # print("body", body)
    # print("headers", headers)
    body = body.replace('"', '\\"')

    # ff : http method, get/post/put...
    ff = reqtxt.split(lb)[0].split(" ")[0]
    ff = ff.lower()
    # print("method:", ff)

    path = reqtxt.split(lb)[0].split(" ")[1]
    # print("path:", path)

    # yz: 结果判定条件
    yz = '0'
    if st is not None and chk is not None:
        yz = 'h1.status_code==' + str(st) + ' and "' + chk + '" in h1.text'
    elif st is not None:
        yz = 'h1.status_code==' + str(st)
    elif chk is not None:
        yz = '"' + chk + '" in h1.text'

    dl = ""
    # ui.dl : 代理
    if prx is not None:
        dl = prx

    with open('模板.txt', 'r', encoding="utf-8") as f1:
        poc_text = f1.read()
    poc_text = poc_text.replace("$body", body).replace("$ff", ff).replace("$path", path).replace("$headers",
                                                                                                 str(headers)) \
        .replace("$yz", yz).replace("$proxy", dl)
    if ff == "get":
        poc_text = poc_text.replace(",data=data", "").replace("data=\"\"", "")
    if dl == "":
        poc_text = poc_text.replace(",proxies=proxies", "").replace(
            "proxies = {'http': 'http://'+proxy, 'https': 'http://'+proxy}", "").replace("proxy=''", "")

    poc_file_name = "poc_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".py"
    file = open('poc/' + poc_file_name, 'w', encoding="utf-8")

    file.write(poc_text)
    file.close()
    # cmd = 'start cmd /k "cd poc & python poc.py -h"'
    # os.system(cmd)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("request", help="请求数据包文件")
    parser.add_argument("-c", "--checker", help="成功时响应包含的关键字(英文区分大小写)，例如：上传成功")
    parser.add_argument("-s", "--status", help="成功时响应码，例如：200", type=int)
    parser.add_argument("-p", "--proxy", help="设置poc使用的proxy, 例如：127.0.0.1:8080")
    parser.add_argument("-m", "--mode", help="处理模式，’0‘代表以字符串格式处理、’1‘代表以二进制格式处理(默认为0)", type=int)
    args = parser.parse_args()

    request_file = args.request
    if args.mode is not None:
        mode = args.mode
    else:
        mode = 0
    if os.path.isfile(request_file):
        if mode == 1:
            print("二进制模式")
            if args.checker is not None or args.status is not None:
                print("响应关键字：", args.checker)
                print("响应码：", args.status)
                get_poc_binay(request_file, args.checker, str(args.status), args.proxy)
            else:
                print("默认使用响应码200作为判定")
                get_poc_binay(request_file, st=str(200), prx=args.proxy)
        elif mode == 0:
            if args.checker is not None or args.status is not None:
                print("响应关键字：", args.checker)
                print("响应码：", args.status)
                get_poc_normal(request_file, args.checker, str(args.status), args.proxy)
            else:
                print("默认使用响应码200作为判定")
                get_poc_normal(request_file, st=str(200), prx=args.proxy)
        else:
            print("mode仅支持’0‘或’1‘")
    else:
        print("请求文件不存在")
