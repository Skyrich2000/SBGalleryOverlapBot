from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import time
from selenium.webdriver.common.action_chains import ActionChains
import cv2
import numpy as np
import random
import os

token = "!.,'-_^*1234567890+="
title = ["싱글벙글 노잼"]
content = ["에휴"]
flag = 0

def addtoken(st):
    out = ""
    for t in st:
        out += t
        if random.choice([True, False]):
            out += token[random.randint(0,len(token)-1)]
    return out

def wait():
    time.sleep(random.randint(4,8)/2)

def isr(t):
    return t in "qwertyuiopasdfghjklzxcvbnm0123456789"

print("토르 킴")
os.popen("/etc/init.d/tor restart")
print("4초 기다림")
time.sleep(4)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--proxy-server=socks5://127.0.0.1:9050")

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=options)

while(True):
    if flag == 0:
        print("시작")
        driver.get('http://icanhazip.com/')
        print("::::IP : ", driver.find_element_by_xpath('/html/body/pre').get_attribute('innerHTML'))

        driver.get('https://gall.dcinside.com/mgallery/board/write/?id=singlebungle1472')
        driver.implicitly_wait(20)
        print("화면 뜸")
        wait()

        try:
            driver.find_element_by_xpath('//*[@id="name"]').send_keys("ㅇㅇ")
            print("닉네임 입력")
            wait()
        except:
            print("닉네임 입력 실패 - 재시작")
            flag = 0
            continue

        try:
            driver.find_element_by_xpath('//*[@id="password"]').send_keys("85749869")
            print("비번 입력")
            wait()
        except:
            print("비번 입력 실패 - 재시작")
            flag = 0
            continue

        #driver.find_element_by_xpath('//*[@id="write"]/div[1]/fieldset/div[3]/ul/li').click()
        #print("말머리 선택")
        #wait()

        try:
            driver.find_element_by_xpath('//*[@id="subject"]').send_keys("싱글벙글 "+random.choice(title))
            print("제목 입력")
            wait()
        except:
            print("제목 입력 실패 - 재시작")
            flag = 0
            continue

    if flag == 0 or flag == 2:
        body = driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="tx_canvas_wysiwyg"]'))
        driver.find_element_by_xpath('/html/body').send_keys(random.choice(content))
        driver.switch_to_default_content()
        print("본문 입력")
        wait()

    if flag == 3:
        while(True):
            driver.execute_script("document.body.style.zoom='350%'")
            try:
                target = driver.find_element_by_xpath('//*[@id="kcaptcha"]')
            except:
                flag = 0
                break
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()
            driver.execute_script("window.scrollBy(100, 100)")
            driver.save_screenshot("screenshot1.png")
            print("스샷 찍음")

            im = Image.open('screenshot1.png').crop((240, 365, 679, 484))
            im = im.filter(ImageFilter.MedianFilter())
            enhancer = ImageEnhance.Contrast(im)
            im = enhancer.enhance(10)
            im.save('temp2.png')

            kernel = np.ones((5, 5), np.uint8)
            im_gray = cv2.imread('temp2.png', cv2.IMREAD_GRAYSCALE)
            im_gray = cv2.morphologyEx(im_gray, cv2.MORPH_CLOSE, kernel)
            (thresh, im_gray) = cv2.threshold(im_gray, 110, 255, cv2.THRESH_BINARY_INV)
            im_gray = cv2.morphologyEx(im_gray, cv2.MORPH_OPEN, kernel)
            _text = pytesseract.image_to_string(im_gray, lang='eng', config='-psm 8 -oem 3 -l eng')

            text = ""
            for t in _text:
                if isr(t):
                    text += t

            print(":", _text, " :"+text)
            if len(text) == 8:
                break

            print("틀려서 클릭후 기다림")
            driver.execute_script("document.body.style.zoom='100%'")
            target.click()
            time.sleep(4)

    if flag == 3:
        try:
            driver.execute_script("document.body.style.zoom='100%'")
            driver.find_element_by_xpath('//*[@id="code"]').send_keys(text)
            wait()
        except:
            flag = 0
            pass


    driver.find_element_by_xpath("//button[@class='btn_blue btn_svc write']").click()
    print("제출 클릭")
        
    
    print("알람 뜰때까지 7초 기다림")
    time.sleep(7)
    try:
        print("알람 확인")
        alert = driver.switch_to.alert
        print(alert.text)
        if "차단" in alert.text:
            print("차단 당해서 IP 바꿔야함")
            flag = 1
        elif "올바른" in alert.text:
            print("기계 인거 들킴")
            flag = 1
        elif "내용" in alert.text:
            print("본문 제대로 안씀")
            flag = 1
        elif "코드" in alert.text or "code" in alert.text:
            print("코드 틀림")
            flag = 3
        alert.accept()
    except:
        print("알림 안뜸 - 제출 성공 or 오류")
        flag = 0
    
    if flag == 1:
        print("시스템 종료")
        pass
