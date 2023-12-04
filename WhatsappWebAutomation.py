from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.parse
import re
import csv
import os


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


def main():
    CHROME_PROFILE_PATH = 'user-data-dir=' + os.path.expanduser('~') + '\\AppData\\Local\\Google' \
                                                                       '\\Chrome\\User Data\\Wtsp'
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)
    driver = webdriver.Chrome(options=options)

    # Define the CSV file containing the phone numbers and the phone row
    csv_file = 'ContactList.csv'
    phone_row = 2
    
    # Gets message from message.txt
    message = open('message.txt', 'r', encoding='utf-8').read()

    # Create empty list to store the phones that couldn't be reached
    phones_that_failed = []

    # Opens the web whatsapp page and waits for the user to scan the QR code
    # if you have already done it recently just wait for one or two seconds
    if qrcode_auth(driver) == 0:

        # If QR scanning succeeds read the csv file with the contacts and star sending the messages
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # skip header row
            for row in reader:
                phone = re.sub(r'\D', '', row[phone_row])
                print(phone)
                try:
                    send_message(driver, phone, message)
                except Exception as e:
                    phones_that_failed.append(phone)
                    print(e)
    else:
        print("QR code failed")

    print("Finished sending the messages\n"
          "Phones that failed: ")
    print(phones_that_failed)


if __name__ == '__main__':
    main()
