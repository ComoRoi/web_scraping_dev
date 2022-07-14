#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import config
import sys
import telegram
import datetime

# 설정값 관리
comConSet = config.COMMON_CONFIG
tele_token = comConSet['tele_token']
chat_id = comConSet['chat_id']
bot = telegram.Bot(token=tele_token)
now = datetime.datetime.now()
nowDatetime = now.strftime('[%Y-%m-%d %H:%M:%S] ')
userPwd = comConSet['userPwd']
targetService = '[WEB Service] '

# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
#options.add_argument("headless")

chrome = Service('/opt/Webdriver/chromedriver')
driver = None
driver = webdriver.Chrome(service=chrome, options=options)
driver.implicitly_wait(7)

def currentTime():
    global nowDatetime
    nowDatetime = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
    return nowDatetime

# USER ID 관리
# argument로 받은 파라메터를 ID로 변환
def setUserId(argument):
    global userId

    if len(arguments) ==1:
        print(currentTime() + targetService + "No Argument")

    elif arguments[1] == "r" or arguments[1] == "R":
        userId = comConSet['userId_1']

    elif arguments[1] == "k" or arguments[1] == "K":
        userId = comConSet['userId_2']

    elif arguments[1] == "s" or arguments[1] == "S":
        userId = comConSet['userId_3']

    elif arguments[1] == "n" or arguments[1] == "N":
        userId = comConSet['userId_4']

    else:
        print(currentTime() + targetService + "Unsupported Argument")

    return userId

arguments = sys.argv

# id를 실제 이름으로 변환
def findName(userName):
    global userKorName

    if userName == 'rsiwin939' :
        userKorName = comConSet['userKorName_1']

    elif userName == 'rsiwin654' :
        userKorName = comConSet['userKorName_2']

    elif userName == 'rshwin1588' :
        userKorName = comConSet['userKorName_3']

    elif userName == 'rshwin777' :
        userKorName = comConSet['userKorName_4']

    else:
        print(currentTime() + targetService + "Unsupported userName")

    return userKorName

# 클립보드에 input을 복사한 뒤
# 해당 내용을 actionChain을 이용해 로그인 폼에 붙여넣기
def copy_input(Id, input):
    pyperclip.copy(input)
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, Id)))
    elem.click()
    time.sleep(10)
    elem.send_keys(Keys.COMMAND, 'v')
    time.sleep(10)


if __name__ == '__main__':

    try :
        driver.get("https://devocean.sk.com/")  # site 접속
        time.sleep(5)

        element = driver.find_element(By.ID, "evnet-popup")
        time.sleep(1)

        # is_displayed metehod check whether the element exists or not and return boolean value.
        displayed = element.is_displayed()

        if (displayed == True):
            elements_xpath = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="evnet-popup"]/div[2]/div[2]/div/div[1]/img')))
            elements_xpath.click()
        else:
            print('not found text, my style php/python *smile*')

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/header/div[1]/div[2]/a[6]'))) # Login을 위한 버튼 선택
        element.click()
        selectLogin = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/header/div[5]/div/div/div[1]/button'))) #팝업챙에서 T아이디 로그인 선택
        selectLogin.click()

    except :
        bot.sendMessage(chat_id=chat_id, text='Can not open login menu.')
        print(currentTime() + targetService + 'Can not open login menu.')

    try :
        #time.sleep(5)
        copy_input("userId", setUserId(arguments)) # id 복사 후 붙여넣기
        copy_input("password", userPwd) # Password 복사 후 붙여넣기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        clickLogin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "authLogin")))
        clickLogin.click()
        time.sleep(5)

    except :
        bot.sendMessage(chat_id=chat_id, text='Can not sent id and Password.')
        print(currentTime() + targetService + 'Can not sent id and Password.')

    try :
        user_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/header/div[2]/div[2]/div[3]/a[1]/span'))) #User 확인을 위한 이름 추출
        time.sleep(5)
        user_box.click()
        userName = user_box.text
        findName(userName)
        user_box1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="userArea"]/div[1]/div[3]/dl[1]/dd/span[1]')))
        bot.sendMessage(chat_id=chat_id, text="Success : " + userKorName + " ; " + user_box1.text)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="userArea"]/div[2]/a/em'))).click()  # 로그아웃 클릭

    except :
        bot.sendMessage(chat_id=chat_id, text= 'Fail : ' + userKorName + " ; " + user_box1.text)
        print(currentTime() + 'Login Fail!!')

time.sleep(5)
driver.quit()
