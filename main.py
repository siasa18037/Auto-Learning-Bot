from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, threading
import random

# Path ของ ChromeDriver
service = Service(r"D:\siasa\vozy\bot\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# login
def login(email, password):
    driver.get("https://app.voxy.com/v2/#/login")

    # รอให้ input อีเมลปรากฏ
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_form_email_input_field"))
    )
    email_input.send_keys(email)

    # กดปุ่ม "ดำเนินการต่อ"
    next_button = driver.find_element(By.ID, "login_form_submit_button")
    driver.execute_script("arguments[0].removeAttribute('disabled')", next_button)  # กรณีปุ่ม disabled
    next_button.click()

    # รอหน้าใส่รหัสผ่าน
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password_input_field"))
    )
    password_input.send_keys(password)

    # กดปุ่ม "ลงชื่อเข้าใช้"
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.voxy-auth-form__submit"))
    )
    login_button.click()

# Run exercises
def run_exercises(driver):
    try:
        h1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[data-test="headline-title"]'))
        )
        exercise_type = h1.text.strip()
        print("🎯 Exercise:", exercise_type)

        if exercise_type == "Bubble Game":
            print("👉 นี่คือ Bubble Game")
            play_bubble_game(driver)
        elif exercise_type == "Video Quiz":
            print("👉 นี่คือ Video Quiz")
            play_bubble_game(driver)
        elif exercise_type == "Meaning Match":
            print("👉 นี่คือ Meaning Match")
            play_grammar_swipe(driver)
        elif exercise_type == "Reading Quiz":
            print("👉 นี่คือ Reading Quiz")
            play_grammar_swipe(driver)
        elif exercise_type == "Pronunciation":
            print("👉 นี่คือ Pronunciation")
            pronunciation(driver)
        elif exercise_type == "Grammar Swipe":
            print("👉 นี่คือ Grammar Swipe")
            play_grammar_swipe(driver)
        elif exercise_type == "Listening Quiz":
            print("👉 นี่คือ Listening Quiz")
            play_grammar_swipe(driver)
        elif exercise_type == "Spelling":
            print("👉 นี่คือ Spelling")
            spelling(driver)
        else:
            print("⚠️ Exercise ประเภทอื่น:", exercise_type)
            run_exercises(driver)
    except Exception:
        print("❌ ไม่เจอ exercise")
        go_next_lesson(driver)

# ฟังก์ชันกด "เริ่มบทเรียนต่อไป"
def go_next_lesson(driver):
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "next-lesson-button"))
        )
        next_button.click()
        print("➡️ กด เริ่มบทเรียนต่อไป")
        time.sleep(0.5)
        start_new_exercise(driver)
    except:
        print("❌ ไม่พบปุ่ม 'เริ่มบทเรียนต่อไป' หาใหม่")
        # go_next_lesson(driver)
        find_lesson(driver)
        start_new_exercise(driver)


# ฟังก์ชันเริ่ม exercise ใหม่
def start_new_exercise(driver):
    try:
        # รอให้ list ของ exercise โหลด
        items = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-test="item-item"]'))
        )

        found = False
        for item in items:
            try:
                # เช็คว่า item นี้มี icon "fa-chevron-right" = ยังเริ่มได้
                icon = item.find_element(By.CSS_SELECTOR, "svg.fa-chevron-right")
                if icon:
                    # ถ้าเจอ → คลิกการ์ดนั้น
                    item.click()
                    print("📌 คลิก Exercise ใหม่เรียบร้อย!")
                    time.sleep(0.5)
                    run_exercises(driver)
                    found = True
                    break
            except:
                continue  # ถ้าไม่มี fa-chevron-right ก็ข้ามไป

        if not found:
            print("⚠️ ไม่มี exercise ที่กดได้ → ไปบทเรียนถัดไป")
            go_next_lesson(driver)

    except Exception as e:
        print("❌ start_new_exercise ล้มเหลว:", e)
        go_next_lesson(driver)

# ฟังก์ชันหา exercise 
def find_lesson(driver):
    try:
        # เข้าไปหน้า catalog ก่อน
        time.sleep(2)
        driver.get("https://app.voxy.com/v2/#/catalog/lesson-lab/")
        time.sleep(2)
        print("🔍 กำลังค้นหาบทเรียนใหม่...")

        found = False
        last_height = driver.execute_script("return document.body.scrollHeight")

        while not found:
            # รอ container หลัก
            container = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.courses-units-list__cards-layout"))
            )

            # ดึง card ทั้งหมด
            cards = container.find_elements(By.CSS_SELECTOR, "div.catalog-card")

            available_lessons = []
            for card in cards:
                text = card.text.strip()
                if "บทเรียนเสร็จสิ้น" in text or "อยู่ระหว่างดำเนินการ" in text:
                    continue
                available_lessons.append(card)

            if available_lessons:
                # เจอบทเรียนใหม่ → สุ่มเลือก
                chosen = random.choice(available_lessons)
                try:
                    btn = chosen.find_element(By.CSS_SELECTOR, 'button[test-id="cta-button"]')
                    driver.execute_script("arguments[0].click();", btn)
                    print("🎯 เข้าไปที่บทเรียนใหม่เรียบร้อย!")
                    found = True
                    break
                except:
                    print("❌ หา button 'ไปที่บทเรียน' ไม่เจอ")
                    return

            # ถ้ายังไม่เจอ → scroll ลง
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # เช็คว่ามีโหลดเพิ่มมั้ย
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("⚠️ ไม่มีบทเรียนใหม่แม้จะเลื่อนสุดแล้ว")
                return
            last_height = new_height

    except Exception as e:
        print("❌ ไม่พบ element หรือเกิดข้อผิดพลาด:", e)
        return

# รอฟังคำสั่งจาก terminal แบบปกติ
def command_listener(driver,mode):
    while True:
        if mode == 'auto':
            print("🔄 คำสั่งอัตโนมัติ...")
            cmd = "autorun"
        else:
            cmd = input("พิมพ์ 'run' เพื่อเริ่ม หรือ autorun หรือ 'exit' เพื่อออก: ").strip().lower()

        # เช็คคำสั่งที่รับมา
        if cmd == "run":
            print("▶️ เริ่มรอบใหม่...")
            start_new_exercise(driver)
        elif cmd == "autorun":
            print("▶️ autorun เริ่มทำงาน...")
            find_lesson(driver)
            start_new_exercise(driver)
        elif cmd == "exit":
            print("🛑 ออกโปรแกรม")
            driver.quit()
            break
        else:
            print("⚠️ คำสั่งไม่ถูกต้อง กรุณาพิมพ์ run หรือ exit")

# Bubble Game
def play_bubble_game(driver):
    print("🚀 เริ่มทำ Bubble Game")

    while True:  # เล่นจนกว่าหมดเกม
        try:
            # รอให้ตัวเลือก 5 ข้อโหลดมา
            options = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input.quiz-radio[data-test="answer-item-button"]'))
            )

            answered = False  # flag เช็คว่าเราตอบไปแล้ว

            for option in options:
                # ข้ามตัวเลือกที่ disabled (ตอบผิดไปแล้ว)
                if not option.is_enabled():
                    continue  

                # คลิกตัวเลือก
                driver.execute_script("arguments[0].click();", option)
                # time.sleep(0.3)

                # คลิกปุ่มยืนยัน
                confirm_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="confirm-button"]'))
                )
                driver.execute_script("arguments[0].click();", confirm_btn)
                print("✅ เลือกคำตอบแล้วกดยืนยัน")

                answered = True
                break  # ออกจาก loop option เพื่อรอผลลัพธ์

            if not answered:
                print("⚠️ ไม่มีตัวเลือกที่ตอบได้แล้ว")
                break

            # --- เช็คว่าถูกหรือผิด ---
            try:
                # ถ้าถูก จะมีปุ่ม "ต่อไป" ปรากฏ
                next_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="next-button"]'))
                )
                driver.execute_script("arguments[0].click();", next_btn)
                print("👉 คำตอบถูก! กดต่อไป")
                # time.sleep(1)
            except:
                # ถ้าไม่เจอปุ่ม "ต่อไป" แปลว่าผิด → จะวนไปเลือกใหม่
                print("❌ คำตอบผิด! ลองตัวเลือกถัดไป")

        except Exception as e:
            print("🎉 เกมจบแล้ว -> ไปบทเรียนถัดไป")
            go_next_lesson(driver)

# Grammar Swipe
def play_grammar_swipe(driver):
    try:
        while True:
            # รอว่าจะยังมีปุ่มตัวเลือกอยู่ไหม
            try:
                options = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[data-test="swipe-card-button"]'))
                )
            except:
                print("✅ ไม่พบการ์ดใหม่ -> จบ Grammar Swipe")
                break

            # เลือกสุ่มจาก options
            choice = random.choice(options)
            print("👉 เลือก:", choice.text)
            choice.click()
            # time.sleep(1)

            # กดปุ่ม "ดำเนินการต่อ"
            try:
                next_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="activity-footer-button"]'))
                )
                next_btn.click()
                print("➡️ กด ดำเนินการต่อ")
                time.sleep(1)
            except:
                print("⚠️ ไม่เจอปุ่ม ดำเนินการต่อ -> ข้ามไป")
                break

    except Exception as e:
        print("🎉 เกมจบแล้ว -> ไปบทเรียนถัดไป")
        go_next_lesson(driver)


# Spelling
def spelling(driver):
    print("🚀 เริ่มทำ Spelling")
    while True:
        try:
            # ดึงปุ่มตัวอักษรทั้งหมด
            letters = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[data-test="bottom-item-letter"]'))
            )

            if len(letters) < 2:
                print("⚠️ ตัวอักษรไม่พอ -> จบเกม")
                break

            # ดับเบิลคลิก 2 ตัวแรก
            for i in range(2):
                driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick', {bubbles: true}));", letters[i])
                print(f"🅰️ ดับเบิลคลิกเลือกตัวอักษร: {letters[i].text}")
                time.sleep(1)

            # กดปุ่ม ตรวจสอบคำตอบ
            send_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="send-button"]'))
            )
            send_btn.click()
            print("✅ กด ตรวจสอบคำตอบ")
            time.sleep(1)

            # เช็คว่าผิดหรือถูก
            try:
                # ถ้า "ดูคำตอบ" โผล่ แสดงว่าผิด
                see_answer_btn = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="see-answer-button"]'))
                )
                see_answer_btn.click()
                print("❌ ผิด -> กด ดูคำตอบ")
                # time.sleep(1)

                next_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="next-button"]'))
                )
                next_btn.click()
                print("➡️ กด ดำเนินการต่อ (หลังผิด)")
                # time.sleep(1)
            except:
                # ไม่เจอปุ่มดูคำตอบ → แสดงว่าถูก
                next_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="next-button"]'))
                )
                next_btn.click()
                print("🎉 ถูกต้อง -> กด ดำเนินการต่อ")
                time.sleep(1)

        except Exception as e:
            print("🎉 เกมจบแล้ว -> ไปบทเรียนถัดไป")
            go_next_lesson(driver)
            break


# Pronunciation
def pronunciation(driver):
    print("🎤 เริ่มทำ Pronunciation")
    while True:
        try:
            # # กดปุ่มบันทึกเสียง
            # record_btn = WebDriverWait(driver, 5).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="record-button"]'))
            # )
            # record_btn.click()
            # print("🔴 เริ่มบันทึกเสียง")

            # time.sleep(3)  # delay 3 วิ เพื่อให้บันทึกเสียง
            # record_btn.click()
            # print("⏹ หยุดบันทึกเสียง")
            # time.sleep(1)  # delay สั้น ๆ ให้ UI อัพเดต

            # # กดปุ่มส่ง
            # send_btn = WebDriverWait(driver, 5).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#next-activity-button[data-test="submit-button"]'))
            # )
            # send_btn.click()
            # print("✅ กด ส่ง")
            # time.sleep(0.5)

            # # กดปุ่มถัดไป (ตรวจสอบทั้ง finish หรือ next)
            # try:
            #     next_btn = WebDriverWait(driver, 5).until(
            #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#next-activity-button[data-test="submit-button"]'))
            #     )
            # except:
            #     # ถ้าไม่มี next → ใช้ finish
            #     next_btn = WebDriverWait(driver, 5).until(
            #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#finish-activity-button[data-test="submit-button"]'))
            #     )

            # next_btn.click()
            # print("➡️ กด ถัดไป")
            # time.sleep(0.5)

            find_lesson(driver)
            start_new_exercise(driver)

        except Exception as e:
            print("🎉 จบ Pronunciation หรือไม่พบ element:", e)
            go_next_lesson(driver)
            break


# เรียก login
login("pre-66010324@kmitl.ac.th", "2568Kmitl")

print("Login เสร็จแล้ว บอทพร้อมทำงาน...")

command_listener(driver,'auto')
