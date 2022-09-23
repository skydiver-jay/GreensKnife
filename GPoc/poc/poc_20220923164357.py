# coding=utf-8
import argparse
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


def req(url):
    data="{\"data\":\"xxxxx\"}"
    proxy='127.0.0.1:8080'
    proxies = {'http': 'http://'+proxy, 'https': 'http://'+proxy}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/json; charset=UTF-8', 'Origin': 'https://test.target.com', 'Referer': 'https://test.target.com'}
    h1=""
    try:
        h1 = requests.post(url+"/testApi",data=data,
                      verify=False, timeout=5,headers=headers,proxies=proxies)
    except  Exception as e:
        print(e)
        return  None
    h1.encoding = "utf-8"
    if h1.status_code==204 and "ok" in h1.text:
        print("[+]漏洞存在:" + url)
        with open('success.txt', 'a+') as f:
            f.write(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="这么说你很勇哦")
    parser.add_argument('-u', '--url', help="目标url，例:https://www.target.com")
    parser.add_argument('-f', '--file', help="目标url文件，一行一个")
    args = parser.parse_args()
    if args.url != None:
        req(str(args.url))

    if args.file != None:
        f = open(str(args.file), 'r')
        for target in f.readlines():
            req(target.strip())