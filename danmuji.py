# -*- coding:utf-8 -*-
#2020年3月25日23:26:34
#作者：ZYY
import requests
import json
from bs4 import BeautifulSoup
import re
import time
#*---------------------------------*-*-*--------------------------------
#语音朗读模块
# 调用百度API
from aip import AipSpeech
from playsound import playsound

# APP_ID API_KEY SECRET_KEY 百度AI提供
APP_ID = '19074101'
API_KEY = 'mutAkjVfxC7f5nfTNjbTLtph'
SECRET_KEY = 'RXlN72QxMHb6FstmzbAGWxW3GzOf93eG'
#连接至百度AI
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def bdyy(info):
    #调用百度AI语音
    result = client.synthesis(info, 'zh', 1, {'vol': '3', 'per': '4'})
    # 识别正确返回语音二进制 错误则返回dict
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
    #播放语音
    playsound('auido.mp3')

#*---------------------------------*-*-*--------------------------------
#输入房间号
print ("请输入房间号:")
bdyy("请输入房间号:")
no = input()

#获取room_id
url2 = "https://live.bilibili.com/" + str(no)
headers2 = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
            'Cookie':r"_uuid=7283B8A0-82F5-1F3A-4925-D390FC6CA9A480540infoc; CURRENT_FNVAL=16; stardustvideo=1; laboratory=1-1; sid=9aipfaaa; rpdid=|(RY~lm~)))0J'ul~lk|mlJJ; CURRENT_QUALITY=116; LIVE_BUVID=24fa57da24620d22365e767dbf87b65f; LIVE_BUVID__ckMd5=deff18f33f64636a; im_notify_type_9046186=0; DedeUserID=9046186; DedeUserID__ckMd5=67c79ca31f83b600; SESSDATA=eacf1b41%2C1580476308%2C60ef7211; bili_jct=07a942cc3c54d0c2029446c9614c90ca; buvid3=DBEFDADA-20D2-4BE1-B56C-B2C1E270C060155811infoc; INTVER=1"
        }
r2 = requests.get(url2,headers = headers2)
html_txt = r2.text
soup = BeautifulSoup(html_txt, "lxml")
src = soup.select("body > div.script-requirement > script:nth-child(1)")
#获取room_id
roomid = re.search(r"\"room_id\":(\d+)", str(src)).group(1)

#提供postdata
postdata = {"roomid":str(roomid),
            "csrf_token":"59a8c7928496ac59980ecfb573f60011",
            "csrf":"59a8c7928496ac59980ecfb573f60011",
            "visit_id":""}
#弹幕列表url
url1 = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'

headers1 = {"Access-Control-Allow-Headers": "Origin,No-Cache,X-Requested-With,If-Modified-Since,Pragma,Last-Modified,Cache-Control,Expires,Content-Type,Access-Control-Allow-Credentials,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Cache-Webcdn,x-bilibili-key-real-ip",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400",
           "Access - Control - Allow - Origin":"https: // live.bilibili.com"}

#*---------------------------------*-*-*--------------------------------
#连接房间
r = requests.post(url1, data=postdata, headers=headers1)
#检测连接是否成功
if r.status_code == 200:
    bdyy("连接成功，房间号"+str(no))
    print ("连接成功，房间号:"+str(no))
    r_txt = r.text
    b = json.loads(r_txt)
    a = re.search(r"\"text\":.*?\"", r_txt).groups()
    #获取用户消息
    msg = b["data"]["room"][-1]["text"]
    #获取用户名称
    name = b["data"]["room"][-1]["nickname"]
    msg1 = msg
    while True:
        #获取弹幕列表
        r = requests.post(url1, data=postdata, headers=headers1)
        #判断获取是否成功
        if r.status_code == 200:
            #取得post包的data
            r_txt = r.text
            #将json转为字典
            b = json.loads(r_txt)
            # 获取用户消息
            msg = b["data"]["room"][-1]["text"]
            # 获取用户名称
            name = b["data"]["room"][-1]["nickname"]
            #判断弹幕是否重复
            if msg == msg1:
                time.sleep(1)
                continue
            #弹幕不重复且昵称和内容长度不超标
            elif msg != msg1 and int(len(name)) <= 10 and int(len(msg)) <= 20:
                name1 = name
                msg1 = msg
                print(name + "说：" + msg)
                bdyy(name + "说" + msg)
        #弹幕获取失败重新获取
        else:
            continue
else:
    bdyy("连接失败，请重试")
    time.sleep(1)
    #退出程序
    exit()