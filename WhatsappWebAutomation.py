from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.parse
import re
import csv
import os
import json


def print_logo():
    print("""
 ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ███╗███████╗
██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗ ████║██╔════╝
██║     ███████║██████╔╝██║   ██║██╔████╔██║█████╗
██║     ██╔══██║██╔══██╗██║   ██║██║╚██╔╝██║██╔══╝
╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
 █████╗ ██╗   ██╗████████╗ ██████╗ ███████╗ █████╗ ██████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗╚══███╔╝██╔══██╗██╔══██╗
███████║██║   ██║   ██║   ██║   ██║  ███╔╝ ███████║██████╔╝
██╔══██║██║   ██║   ██║   ██║   ██║ ███╔╝  ██╔══██║██╔═══╝
██║  ██║╚██████╔╝   ██║   ╚██████╔╝███████╗██║  ██║██║
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝

""")


def qrcode_auth(driver):
    try:
        driver.get("https://web.whatsapp.com/")
        while len(driver.find_elements(By.ID, 'side')) < 1:
            time.sleep(1)
        return 0
    except:
        return 1


def send_message(driver, phone, message):
    message = urllib.parse.quote(message)
    link = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
    driver.get(link)
    while len(driver.find_elements(By.ID, 'side')) < 1:
        time.sleep(1)

    while len(driver.find_elements(By.LINK_TEXT, 'Iniciando conversa')) > 0:
        time.sleep(1)

    time.sleep(3)
    send_message_button = driver.find_element(By.XPATH,
                                              '//*[@id="main"]/footer/div[1]/div/span[2]'
                                              '/div/div[2]/div[2]/button/span')
    send_message_button.click()
    print('Message sent to:' + phone)
    time.sleep(2)


def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def main():
    print_logo()
    user = input('PRESS ENTER TO START SENDING THE MESSAGES')
    config = load_config()
    CHROME_PROFILE_PATH = 'user-data-dir=' + os.path.expanduser('~') + '\\AppData\\Local\\Google' \
                                                                       '\\Chrome\\User Data\\Wtsp' + user
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)
    driver = webdriver.Chrome(options=options)

    # Define the CSV file containing the phone numbers and the phone row
    csv_file = config["csv_file"]
    phone_row = config["phone_row"]
    message_file = "message.txt"
    
    # Gets message from the message file
    message = open(message_file, 'r', encoding='utf-8').read()

    # Create empty list to store the phones that couldn't be reached
    phones_that_failed = []

    if qrcode_auth(driver) != 0:

        print("QR code failed")
    # Opens the web whatsapp page and waits for the user to scan the QR code
    # if you have already done it recently just wait for one or two seconds
    else:
        # If QR scanning succeeds read the csv file with the contacts and star sending the messages
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # skip header row
            for row in reader:
                phone = re.sub(r'\D', '', row[phone_row])
                try:
                    send_message(driver, phone, message)
                except Exception as e:
                    phones_that_failed.append(phone)
                    print("Failed to send message to: " + phone)

    print("Finished sending the messages\n"
          "Phones that failed: ")
    print(phones_that_failed)
    input("You can close this window")

    while True:
        pass


if __name__ == '__main__':
    main()
