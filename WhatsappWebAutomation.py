import csv
import json
import os
import re
import time
import urllib.parse
import shutil

from tkinter import Tk, ttk

from selenium import webdriver
from selenium.webdriver.common.by import By


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

Not intended for spamming use consented data only.
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

    while len(driver.find_elements(By.ID, 'main')) < 1:
        time.sleep(1)

    send_message_button = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]'
                                                       '/div/div[2]/div[2]/button/span')
    send_message_button.click()
    print('Message sent to:' + phone)
    time.sleep(2)


def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def delete_chrome_profile(profile_path):
    try:
        shutil.rmtree(profile_path, ignore_errors=True)
        print("Old QR settings cleaned")
    except:
        print("Couldn't generate ner QR, contact developer")


def start_menu():
    print_logo()
    user = input('PRESS ENTER TO START\n\n')

    option = [""]

    def scan_new_qr():
        option[0] = "new_qr"
        root.destroy()
    def use_old_qr():
        option[0] = "same_qr"
        root.destroy()

    root = Tk()
    frm = ttk.Frame(root, padding=50)
    frm.grid()

    ttk.Button(frm, text="Scan a New QR Code", command=scan_new_qr).grid(column=0, row=0, pady=10)
    ttk.Button(frm, text="Continue Without Scanning", command=use_old_qr).grid(column=0, row=1, pady=10)

    root.mainloop()

    return option[0]


def main():
    # If new qr code is requested. Clean up the profile directory
    if start_menu() == "new_qr":
        profile_path = os.path.expanduser('~') + '\\AppData\\Local\\Google\\Chrome\\User Data\\Wtsp'
        print("Cleaning up old QR settings")
        delete_chrome_profile(profile_path)

    CHROME_PROFILE_PATH = 'user-data-dir=' + os.path.expanduser('~') + '\\AppData\\Local\\Google' \
                                                                       '\\Chrome\\User Data\\Wtsp'
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)
    driver = webdriver.Chrome(options=options)

    config = load_config()
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
    input("\nYou can close this window")

    while True:
        pass


if __name__ == '__main__':
    main()
