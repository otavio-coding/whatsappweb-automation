from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib
import re
import csv


def qrcode_auth():
    try:
        CHROME_PROFILE_PATH = 'user-data-dir=C:\\Users\\myname\\AppData\\Local\\Google\\Chrome\\User Data\\Wtsp'
        options = webdriver.ChromeOptions()
        options.add_argument(CHROME_PROFILE_PATH)
        driver = webdriver.Chrome(options=options)
        driver.get("https://web.whatsapp.com/")
        while len(driver.find_elements(By.ID, 'side')) < 1:
            time.sleep(1)
        return 0
    except:
        return 1


def send_message(phone, message):
    CHROME_PROFILE_PATH = 'user-data-dir=C:\\Users\\myname\\AppData\\Local\\Google\\Chrome\\User Data\\Wtsp'
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)
    driver = webdriver.Chrome(options=options)

    message = urllib.parse.quote(message)
    link = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
    driver.get(link)
    while len(driver.find_elements(By.ID, 'side')) < 1:
        time.sleep(1)

    time.sleep(5)
    send_message_button = driver.find_element(By.XPATH,
                                              '//*[@id="main"]/footer/div[1]/div/span[2]'
                                              '/div/div[2]/div[2]/button/span')
    send_message_button.click()
    time.sleep(2)


def main():
    # Define the CSV file containing the phone numbers and the phone row
    csv_file = 'ContactList.csv'
    phone_row = 2

    # Define the message you want to send
    message = "Example Message\n\n" \
              "Date: [Start Date] to [End Date]\n\n" \
              "The upcoming [presentation/event] will focus on a '*Topic*.' Participants are encouraged to present " \
              "either an invented or an existing *item* with improvements.\n" \
              "During the [presentation/event], emphasize the *item*'s benefits, pricing, features, and unique " \
              "aspects using persuasive and clear language to engage the audience.\n\n" \
              "Requirements: Prepare a [Presentation Time]-minute [presentation/speech] with visual aids " \
              "(e.g., slides) and a written component (minimum [Word Count] words).\n\n" \

    # Create empty list to store the phones that couldn't be reached
    phones_that_failed = []

    # Opens the web whatsapp page and waits for the user to scan the QR code
    # if you have already done it recently just wait for one or two seconds
    if qrcode_auth() == 0:

        # If QR scanning succeeds read the csv file with the contacts and star sending the messages
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # skip header row
            for row in reader:
                phone = re.sub(r'\D', '', row[phone_row])
                print(phone)
                try:
                    send_message(phone, message)
                except:
                    phones_that_failed.append(phone)
    else:
        print("QR code failed")

    print("Finished sending the messages\n"
          "Phones that failed: ")
    print(phones_that_failed)


if __name__ == '__main__':
    main()
