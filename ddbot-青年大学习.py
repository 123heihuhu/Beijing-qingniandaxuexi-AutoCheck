from base64 import urlsafe_b64decode
from cgitb import reset
from decimal import DivisionByZero
from email import contentmanager
from lib2to3.pgen2 import driver
from socket import MsgFlag
from sys import path
from DingDingBot.DDBOT import DingDing
from pandas.io import html
import requests
import smtplib
from lxml import etree
from time import sleep
import pytesseract
from PIL import Image, ImageEnhance
from requests.sessions import Session
from selenium import webdriver
from utility import encrypt, cap_recognize
import time
import traceback
import pandas as pd
import os
import json
import re
import hmac
import hashlib
import base64
import urllib.parse
from bs4 import BeautifulSoup
import random
username =""  #用户名-改成自己的
password =""   #密码-改成自己的
org_id =                  #组织id
ua = os.getenv('Useer-Agent',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111')
namelist=[]
backmessage=""
setfinish =[]
str3=""


'''def Send_DD(note):
    print(note)
    # 初始话DingDingBOt  webhook是钉钉机器人所必须的
    dd = DingDing(webhook='https://oapi.dingtalk.com/robot/send?access_token=f3e149a75357125b16f85c721cbfc082cbf918eaa6768d0232e6')
    # 发送文本消息
    print(dd.Send_Text_Msg(content="测试钉钉",atMobiles=["13161"]))'''
def sign(secret,timestamp): 
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # print(timestamp)
    # print(sign)
    sign_str= {"sign": sign,"timestamp":timestamp}
    return sign_str

# 钉钉消息
def send_msg(sign,timestamp,str):
    tim = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    headers = {"Content-Type": "application/json"}
    data = {
     "msgtype": "markdown",
     "markdown": {
         "title":"大学习", ##与关键字一致
         "text": "#### 完成名单青年大学习  \n> "+ str +"\n\n>"
     },
     # @群内人员
      # "at": {
      #     "atMobiles": [
      #         "150XXXXXXXX"
      #     ],
      #     "atUserIds ": [
      #         "user123"
      #     ],
      #     "isAtAll": false
      # }
    }
    webh = webhook+'&timestamp='+timestamp+'&sign='+sign
    r = requests.post(webh, data=json.dumps(data), headers=headers)
    print(r.text)


# 时间戳
timestamp = str(round(time.time() * 1000))
# 钉钉机器人配置
secret = ''
webhook = ''
sign_str =sign(secret,timestamp)
sg = sign_str['sign']


def study(username, password, org_id, ua):         ####获取完成名单信息
    driver =("https://www.bjyouth.net/site#")
    
    # return 1:success;0:fail
    url = ''
    try_time = 0
    headers ={'Useer-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111'}
    while try_time < 4:
        try:
            bjySession = requests.session()
            bjySession.timeout = 5  # set session timeout
            bjySession.headers.update({"User-Agent": ua, })
            touch = bjySession.get(url="https://www.bjyouth.net/site#")
            cap_url = "https://www.bjyouth.net/" + re.findall(
                r'src="(/site/captcha.+)" alt=', touch.text)[0]
            print(cap_url)
            cap_text = cap_recognize(bjySession.get(url=cap_url).content)
            print(f'验证码识别: {cap_text}')
            #print(bjySession.cookies.get_dict(path=path))
            login_r = bjySession.post('https://www.bjyouth.net/site/loginnn',
                                      data={
                                          #'_csrf': bjySession.cookies.get_dict()['cookie'],
                                          'Login[password]': encrypt(password),
                                          'Login[username]': encrypt(username),
                                          'Login[verifyCode]': cap_text
                                      })
            print(f'Login:[{login_r.status_code}]{login_r.text}')
            if login_r.text == '8':
                print('Login:识别的验证码错误')
                continue
            if 'fail' in login_r.text:
                try_time += 9
                raise Exception('Login:账号密码错误')                                           ###初期登录可能需要手机验证码，请先手动登陆一次后再使用
            break
        except:
            time.sleep(3)
            try_time += 1
            print(traceback.format_exc())
        
    res = bjySession.get("https://www.bjyouth.net/statistics/dxx-mine",headers=headers)
    #print(res.text)
    
    for Name in namelist:
        if Name in res.text:
            setfinish.append(Name)    ####查询完成名单
    print(setfinish)
    str3 ="++".join(setfinish)        ####列表转换字符串
    print(str3)
    send_msg(sg,timestamp,str3)
    driver.close()

study(username, password, org_id, ua)
