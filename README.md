# 实验四 TCP 文件下载
## 要求
基于 TCP 的文件下载。客户端向服务器发送一个用户输入的文件名，若文件存在，则下载文件，若不存在，则提示用户。 服务端接收客户端数据，识别并显示客户端所请求下载的文件名，若文件存在， 则发送给客户端，若不存在，则提示用户。
## 注意点


## 完成情况
字节传输文件，SSL加密，list查询文件，异常抛出，哈希校验文件传输是否有误

## SSL 证书生成
`openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key`

    Country Name (2 letter code) [AU]:CN   
    State or Province Name (full name) [Some-State]:CD
    Locality Name (eg, city) []:CD
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:rrrfly
    Organizational Unit Name (eg, section) []:rrrfly
    Common Name (e.g. server FQDN or YOUR name) []:localhost
    Email Address []:rrrfly@163.com

这里的`Common Name` 如果在本地就要使用`localhost`

上面的字段分别是
国家、州、地区、组织名称、组织单位名称、公用名、Email

`openssl x509 -in server.crt -text -noout` 查看证书生成的内容

## server client是不存在SSL的，也就是数据是明文传输
流量包是`NoSSL.pcapng`

## server1 client1存在SSL，也就是数据经过加密传输
流量包是`SSL.pcapng`

## 流量包抓取的注意点
使用 `wirshark` 的 `Adapter for loopback traffic capture` 网卡