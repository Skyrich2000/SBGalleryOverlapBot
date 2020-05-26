from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from PIL import Image, ImageEnhance, ImageFilter
from selenium import webdriver
import numpy as np
import pytesseract
import random
import time
import cv2
import os

token = "!.,'-_^*1234567890+="
title = ["노잼", "망함"]
content = ["작작해"]
flag = 0
retry = 0

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

print(os.popen("/etc/init.d/tor start").readline())
print("토르 켜질때 까지 20초 기다림")
time.sleep(20)

options = webdriver.ChromeOptions()
options.add_argument("\"accept\"=*/*")
options.add_argument("accept-encoding=\"sdch\"")
options.add_argument("accept-language=ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
options.add_argument('window-size=800x600')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
#options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
options.add_argument("--proxy-server=socks5://127.0.0.1:9050")

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",chrome_options=options)
#
print("시작")
driver.get('http://icanhazip.com/')
print("::::IP : ", driver.find_element_by_xpath('/html/body/pre').get_attribute('innerHTML'))

driver.get('https://gall.dcinside.com/mgallery/board/lists?id=singlebungle1472')
time.sleep(15)
print("메인 페이지")
wait()
"""
driver.find_element_by_xpath('//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[3]/td[3]/a[1]').click()
time.sleep(20)
print("아무 페이지")
wait()
"""
while(True):
    if flag == 0:
        driver.find_element_by_xpath('//*[@id="container"]/section/header/div/div[1]/h2/a').click()
        time.sleep(15)
        print("다시 메인 페이지")
        wait()

        driver.find_element_by_xpath('//*[@id="container"]/section[1]/article[2]/div[1]/div[3]/div/div[2]/a').click()
        print("화면 뜸 - 20초 대기")
        time.sleep(20)

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
        body = driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tx_canvas_wysiwyg"]'))
        driver.find_element_by_xpath('/html/body').send_keys(random.choice(content))
        driver.switch_to.default_content()
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

            im = Image.open('screenshot1.png').crop((374, 660, 805, 770))
            im = im.filter(ImageFilter.MedianFilter())
            enhancer = ImageEnhance.Contrast(im)
            im = enhancer.enhance(10)
            im.save('temp2.png')

            kernel = np.ones((5, 5), np.uint8)
            
            im_gray = cv2.imread('temp2.png', cv2.IMREAD_GRAYSCALE)
            (thresh, im_gray) = cv2.threshold(im_gray, 110, 255, cv2.THRESH_BINARY_INV)
            im_gray = cv2.morphologyEx(im_gray, cv2.MORPH_OPEN, kernel)
            _text = pytesseract.image_to_string(im_gray, lang='eng', config='-psm 8 -oem 3 -l eng')
            cv2.imwrite("tt.png", im_gray)

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
            driver.find_element_by_xpath('//*[@id="code"]').clear()
            wait()
            driver.find_element_by_xpath('//*[@id="code"]').send_keys(text)
            wait()
        except:
            flag = 0
            pass

    driver.execute_script("window.scrollBy(100, 100)")
    wait()
    ele = driver.find_element_by_xpath('//*[@id="write"]/div[4]/button[1]')
    actions = ActionChains(driver)
    actions.move_to_element(ele)
    actions.perform()
    wait()
    ele = driver.find_element_by_xpath('//*[@id="write"]/div[4]/button[2]')
    actions = ActionChains(driver)
    actions.move_to_element(ele)
    actions.perform()
    ele.click()
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
            if flag == 5:
                print("기계 인거 들킴 - 다시 클릭", retry)
                retry += 1
                flag = 5
                if retry > 2:
                    print("기계 인거 들킴2 - 글 첨부터 쓰기")
                    retry = 0
                    flag = 0
            else:
                print("기계 인거 들킴 - 다시 클릭")
                flag = 5 #한번더
        elif "내용" in alert.text:
            print("본문 제대로 안씀 - 글 첨부터 쓰기")
            flag = 0
        elif "코드" in alert.text or "code" in alert.text:
            print("코드 틀림")
            flag = 3
        wait()
        alert.accept()
        wait(), wait()
    except:
        print("알림 안뜸 - 제출 성공 or 오류")
        flag = 0

    if flag == 1:
        driver.quit()
        print("시스템 종료")
        break
