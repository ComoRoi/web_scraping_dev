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
options.add_argument("headless")

chrome = Service('/opt/Webdriver/chromedriver')
driver = webdriver.Chrome(service=chrome, options=options)
#driver.implicitly_wait(7)

def currentTime():
    global nowDatetime
    nowDatetime = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
    return nowDatetime

# USER ID 관리
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

#클립보드에 input을 복사한 뒤
#해당 내용을 actionChain을 이용해 로그인 폼에 붙여넣기
def copy_input(Id, input):
    pyperclip.copy(input)
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, Id)))
    elem.click()
    elem.send_keys(Keys.COMMAND, 'v')
    time.sleep(7)

if __name__ == '__main__':

    try :
        driver.get("https://devocean.sk.com/")
        time.sleep(7)

    except :
        bot.sendMessage(chat_id=chat_id, text='Selenium can not open the web.')
        print(currentTime() + targetService + 'Selenium can not open the web.')

    try :
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/header/div[1]/div[2]/a[6]')))
        element.click()

    except :
        bot.sendMessage(chat_id=chat_id, text='Can not open login menu.')
        print(currentTime() + targetService + 'Can not open login menu.')

    try :
        copy_input("userId", setUserId(arguments))
        copy_input("password", userPwd)
        clickLogin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "authLogin")))
        clickLogin.click()
        time.sleep(7)

    except :
        bot.sendMessage(chat_id=chat_id, text='Can not sent id and Password.')
        print(currentTime() + targetService + 'Can not sent id and Password.')

    try :
        user_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "user-box")))
        user_box.click()
        time.sleep(7)
        bot.sendMessage(chat_id=chat_id, text="Success : " + user_box.text)

    except :
        bot.sendMessage(chat_id=chat_id, text= 'Fail : ' + user_box.text)
        print(currentTime() + 'Login Fail!!')

driver.quit()
