## 方案V2： Clash & pcap2socks YYDS！
### 依赖
1. （可选）Clash： [https://github.com/Dreamacro/clash/releases/tag/v1.13.0](https://github.com/Dreamacro/clash/releases/tag/v1.13.0)

2. pcap2socks: [https://github.com/zhxie/pcap2socks/releases/tag/v0.6.2](https://github.com/zhxie/pcap2socks/releases/tag/v0.6.2)

3. 已有梯子：如果梯子已经是socks server，则可省掉Clash；如果梯子是诸如VPN的全局隧道，则需要Clash，本方案描述的是后者场景。

### 使用方法

1. 将PC和Switch等游戏主机连接至同一局域网。
2. 可选将Clash运行在本地PC或远端VPN Server（如果可控的话）上，区别就是访问socks代理的IP不同。
 ````
命令行直接运行Clash程序（如clash-windows-386.exe） ，即可启动一个socks server并监听在7890端口。

如需定制配置可参考：https://github.com/Dreamacro/clash/wiki/Configuration
 ````
3. 在PC上命令行运行pcap2socks，规则如下：
````
pcap2socks.exe -s 172.24.10.10 -p 172.24.11.11 -d 127.0.0.1:7890

其中，172.24.10.10为Switch需要配置的IP地址，172.24.11.11为Switch需要配置的网关，掩码可以配成255.255.0.0，DNS配成8.8.8.8；
127.0.0.1:7890为socks server，根据实际情况设置。

tips：如果PC上存在多个可用网络，直接运行上述命令会出错，可以通过-i参数指定网卡。
````
4. 修改游戏主机网络配置（类似UU），即可连接成功。

#### 当然这个方案可以用于同局域网下所有可支持配置网络的设备共享梯子。
