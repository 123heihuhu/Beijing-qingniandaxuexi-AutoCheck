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
username ="wangluo201"  #用户名-改成自己的
password ="20wangluo1"   #密码-改成自己的
org_id = 3574589
ua = os.getenv('Useer-Agent',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111')
namelist=["邵雨晨","周帅","张聪","白冠宇","白茹菲","刘京","马俊然","王珺璋","王岩","王子昕","吴宇涵","马思源"]
backmessage=""
setfinish =[]
str2=""
def study(username, password, org_id, ua):
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
            #https://www.bjyouth.net/site/captcha?v=61d92953ed4d90.38663537
            #https://m.bjyouth.net/site/captcha?v=61d92a1ca8fea5.53218211
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
                raise Exception('Login:账号密码错误')
            break
        except:
            time.sleep(3)
            try_time += 1
            print(traceback.format_exc())
        
    res = bjySession.get("https://www.bjyouth.net/statistics/dxx-mine",headers=headers)
    #print(res.text)
    for Name in namelist:
        if Name in res.text:
            setfinish.append(Name)
        print(setfinish)
    driver.close()
    return setfinish
'''def Send_DD(note):
    print(note)
    # 初始话DingDingBOt  webhook是钉钉机器人所必须的
    dd = DingDing(webhook='https://oapi.dingtalk.com/robot/send?access_token=f3e149a75357125b16f85c721cbfc082cbf918eaa6768d0232e6bb0379ab7111')
    # 发送文本消息
    print(dd.Send_Text_Msg(content="测试钉钉",atMobiles=["13161365667"]))'''

def sendDing(msg):
    '''
    发送钉钉消息功能
    '''
    dingding_url = 'https://oapi.dingtalk.com/robot/send?access_token=f3e149a75357125b16f85c721cbfc082cbf918eaa6768d0232e6bb0379ab7111'
    data = {"msgtype": "text","text": {"content": "learn:"+str(msg)}}
    headers = {'Content-Type':'application/json;charset=UTF-8'}
    send_data = json.dumps(data).encode('utf-8')
    ret = requests.post(url=dingding_url,data=send_data,headers=headers)
    print(ret.text)
study(username, password, org_id, ua)
sendDing("learn")