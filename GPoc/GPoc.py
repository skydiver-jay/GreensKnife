# coding=utf-8
import argparse
import os
import time


def get_poc(req, chk=None, st=None, prx=None):

    reqtxt = req
    c = 0
    body = ""
    headers = {}
    for i in reqtxt.split("\n"):
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
    ff = reqtxt.split("\n")[0].split(" ")[0]
    ff = ff.lower()
    # print("method:", ff)

    path = reqtxt.split("\n")[0].split(" ")[1]
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
    args = parser.parse_args()

    request_file = args.request
    if os.path.isfile(request_file):
        with open(request_file, 'r', encoding="utf-8") as f1:
            text = f1.read()
        # print("处理request数据包")
        if args.checker is not None or args.status is not None:
            print("响应关键字：", args.checker)
            print("响应码：", args.status)
            get_poc(text, args.checker, args.status, args.proxy)
        else:
            print("默认使用响应码200作为判定")
            get_poc(text, st=200, prx=args.proxy)
