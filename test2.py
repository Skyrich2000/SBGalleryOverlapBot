from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import time
from selenium.webdriver.common.action_chains import ActionChains
import cv2
import numpy as np
import random

token = "!.,'-_^*1234567890+="
title = []
content = []
flag = False

def addtoken(st):
    out = ""
    for t in st:
        out += t
        if random.choice([True, False]):
            out += token[random.randint(0,len(token)-1)]
    return out

def wait():
    time.sleep(random.randint(2,6)/2)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
options.add_argument('headless')
options.add_argument("disable-gpu")
#options.add_argument("--proxy-server=socks5://127.0.0.1:9150")

driver = webdriver.Chrome(chrome_options=options)

while(True):
    print("시작")
    driver.get('http://icanhazip.com/')
    print("::::IP : ", driver.find_element_by_xpath('/html/body/pre').get_attribute('innerHTML'))

    driver.get('https://gall.dcinside.com/mgallery/board/write/?id=singlebungle1472')
    driver.implicitly_wait(20)
    print("화면 뜸")
    wait()

    driver.find_element_by_xpath('//*[@id="name"]').send_keys("ㅇㅇ")
    print("닉네임 입력")
    wait()

    driver.find_element_by_xpath('//*[@id="password"]').send_keys("85749869")
    print("비번 입력")
    wait()

    driver.find_element_by_xpath('//*[@id="write"]/div[1]/fieldset/div[3]/ul/li').click()
    print("말머리 선택")
    wait()

    driver.find_element_by_xpath('//*[@id="subject"]').send_keys("싱글벙글 "+random.choice(title))
    print("제목 입력")
    wait()

    while(True):
        body = driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="tx_canvas_wysiwyg"]'))
        driver.find_element_by_xpath('/html/body').send_keys(random.choice(content))
        driver.switch_to_default_content()
        print("본문 입력")
        wait()

        driver.find_element_by_xpath("//button[@class='btn_blue btn_svc write']").click()
        print("제출 클릭")
        
        print("알람 뜰때까지 7초 기다림")
        time.sleep(7)
        try:
            print("알람 확인")
            alert = driver.switch_to.alert
            print(alert.text)
            if "차단" in alert.text:
                print("IP 바꿔야함")
                flag = True
            alert.accept()
            print("본문 내용 다시 입력")
        except:
            print("알림 안뜸 - 제출 성공?")
            break
    
    #if flag:
        