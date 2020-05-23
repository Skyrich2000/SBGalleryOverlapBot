while(True):
            time.sleep(random.randint(1,4)/2)
            driver.execute_script("document.body.style.zoom='350%'")
            target = driver.find_element_by_xpath('//*[@id="kcaptcha"]')
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
            cv2.imwrite("tt.png", im_gray)
            _text = pytesseract.image_to_string(im_gray, lang='eng', config='-psm 8 -oem 3 -l eng')

            text = ""
            for t in _text:
                if t.isalpha() or t.isdigit():
                    text += t

            print(":", _text, " :",text)
            if len(text) == 8 :
                break

            print("틀려서 클릭후 기다림")
            driver.execute_script("document.body.style.zoom='100%'")
            target.click()
            time.sleep(5)

        time.sleep(random.randint(1, 4)/2)
        driver.execute_script("document.body.style.zoom='100%'")
        driver.find_element_by_xpath('//*[@id="code"]').send_keys(text)
        time.sleep(random.randint(1, 4)/2)
        driver.find_element_by_xpath("//button[@class='btn_blue btn_svc write']").click()    
        print("제출 클릭")