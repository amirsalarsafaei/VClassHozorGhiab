# -*- coding: utf-8 -*-
import datetime

from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


class Message:
    def __init__(self, messageId, userId, text, username, date):
        self.messageId = messageId
        self.userId = userId
        self.content = text
        self.username = username
        self.date = date


name = input("نام خود را وارد کنید")
student_number = input("شماره دانشجویی خود را وارد کنید")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://vc.sharif.edu/ch/t.mogtaba-ta")

guest_btn = driver.find_element(by=By.ID, value="btn_guest")

guest_btn.click()
time.sleep(1)
name_field = driver.find_element(by=By.XPATH,
                                 value="/html/body/div[5]/div[2]/div/input")
time.sleep(1)
name_field.send_keys(name)

name_field_btn = driver.find_element(by=By.XPATH,
                                     value="/html/body/div[5]/div[3]/div[2]/button")
time.sleep(1)
name_field_btn.click()

message_box = driver.find_element(by=By.XPATH,
                                  value="/html/body/div[2]/div[1]/div[2]/div[1]/div[4]/div[2]/div/div[2]/div["
                                        "3]/div[1]")
send_message_btn = driver.find_element(by=By.XPATH,
                                       value="/html/body/div[2]/div[1]/div[2]/div[1]/div[4]/div[2]/div/div[2]/div["
                                             "3]/div[4]/button")


def send_message(message):
    time.sleep(1)
    message_box.send_keys(message)
    time.sleep(0.5)
    send_message_btn.click()


chatBox = driver.find_element(by=By.XPATH,
                              value="/html/body/div[2]/div[1]/div[2]/div[1]/div[4]/div[2]/div/div[1]/div[2]")
chatBox = chatBox.find_element(by=By.CLASS_NAME, value="message-box-content")
messages_web = chatBox.find_elements(by=By.CLASS_NAME, value="chat-msg")
send_message("سلام استاد")
while (True):
    time.sleep(15)
    messages = []
    chatBox = driver.find_element(by=By.XPATH,
                                  value="/html/body/div[2]/div[1]/div[2]/div[1]/div[4]/div[2]/div/div[1]/div[2]")
    chatBox = chatBox.find_element(by=By.CLASS_NAME, value="message-box-content")
    messages_web = chatBox.find_elements(by=By.CLASS_NAME, value="chat-msg")
    for message in messages_web:

        date = message.find_element(by=By.XPATH, value="div[2]/span")

        ActionChains(driver) \
            .move_to_element(date) \
            .perform()
        date_str = unidecode(date.text)
        print(date_str)
        messages.append(Message(messageId=message.get_attribute("data-message-id"),
                                userId=message.get_attribute("data-userid"),
                                text=message.find_element(by=By.CLASS_NAME, value="text").text,
                                username=message.find_element(by=By.CLASS_NAME, value="username").text,
                                date=datetime.datetime.strptime(date_str, "%H:%M")))
    cntCode = 0
    cntCodeAndName = 0

    for i in range(min(9, len(messages))):
        tmp = messages[len(messages) - i-1].content
        if len(tmp) < 8:
            continue
        for j in range(len(tmp) - 8):
            if not (tmp[j] == '4' or tmp[j] == '9'):
                continue
            if tmp[j:j + 8].isnumeric():
                if len(tmp) - 14 > 3:
                    print(len(tmp))
                    cntCodeAndName += 1
                else:
                    cntCode += 1
                if cntCode + cntCodeAndName == 4:
                    lastDate = messages[len(messages) - i].date
                break
    response = ""
    if cntCodeAndName + cntCode > 3:
        response += student_number + " "
    if cntCodeAndName > 4:
        response += name
    if len(response) == 0:
        continue
    print((datetime.datetime.now() - lastDate).total_seconds() % (24 * 3600))
    if ((datetime.datetime.now() - lastDate).total_seconds() % (24 * 3600)) > 270:
        continue
    send_message(response)
    time.sleep(500)