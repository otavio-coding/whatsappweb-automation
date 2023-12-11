import csv
import json
import os
import re
import time
import urllib.parse
import shutil
import threading

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

from selenium import webdriver
from selenium.webdriver.common.by import By


def load_config(file_path='inputFiles/config.json'):
    """Reads the config file."""
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def qrcode_auth(driver):
    """Opens whatsapp web and waits for the user to scan a QR code."""
    try:
        driver.get("https://web.whatsapp.com/")
        while len(driver.find_elements(By.ID, 'side')) < 1:
            time.sleep(1)
        return {"value": 0, "text": "Qr code scanned successfully"}
    except Exception as e:
        tk.messagebox.showerror("Error", f"Program Error:{e}\nPlease restart the app.")
        return {"value": 1, "text": "QR code scanning failed"}


def delete_chrome_profile(profile_path):
    """Deletes the path of the cached qr code so the user can scan a new one."""
    try:
        shutil.rmtree(profile_path, ignore_errors=True)
        return "Old QR settings cleaned"
    except Exception as e:
        tk.messagebox.showerror("Error", f"Program Error:{e}\nPlease restart the app.")


def send_message(driver, phone, message, label):
    """Send message defined in message.txt to the phone using selenium."""

    def is_number_invalid():
        return len(driver.find_elements(By.CSS_SELECTOR, invalid_number_selector)) > 0

    def handle_invalid_number():
        label.config(text='*****-**** is an invalid number.')

    def is_send_button_present():
        return len(driver.find_elements(By.XPATH, send_button_XPATH)) > 0

    def click_send_button():
        send_message_button = driver.find_element(By.XPATH, send_button_XPATH)
        send_message_button.click()
        label.config(text='Message sent to: *****-****')
        time.sleep(2)

    # define the variables we'll be checking on the page
    invalid_number_selector = "div.f8jlpxt4.iuhl9who"  # Appears as a pop-up box if the number is invalid.
    starting_chat_selector = 'div.du8bjn1j.p9fp32ui.m1e7cby3.htjsae3x.ljrqcn24'  # Appears when the chat is loading.
    send_button_XPATH = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'

    label.config(text='Sending message to: *****-****. Please wait...')
    message = urllib.parse.quote(message)
    link = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
    driver.get(link)

    # Due to whatsapp website unpredictability, we have to do multiple checkS on what's available on the screen

    while len(driver.find_elements(By.ID, 'side')) < 1:
        time.sleep(1)
    time.sleep(1)
    while len(driver.find_elements(By.ID, 'main')) < 1:
        # wait until the chat box is available.
        if len(driver.find_elements(By.CSS_SELECTOR, starting_chat_selector)) > 0:
            while len(driver.find_elements(By.CSS_SELECTOR, starting_chat_selector)) > 0:
                time.sleep(1)

            if is_number_invalid():
                handle_invalid_number()
                return -1

            elif is_send_button_present():
                click_send_button()
                return 0

        if is_number_invalid():
            handle_invalid_number()
            return -1

        elif is_send_button_present():
            click_send_button()
            return 0

    if is_number_invalid():
        if is_send_button_present():
            time.sleep(1)
            click_send_button()
            return 0
        else:
            handle_invalid_number()
            return -1

    if is_send_button_present():
        time.sleep(1)
        click_send_button()
        return 0


def log_failures(phones_that_failed):
    with open('outputFiles/phones_that_failed.csv', 'w', newline="") as log:
        writer = csv.writer(log, delimiter=';')
        writer.writerow(["Failed Phones"])
        writer.writerows([[phone] for phone in phones_that_failed])


def main(option, label, success_label, failure_label, pb):
    profile_path = os.path.expanduser('~') + '\\AppData\\Local\\Google\\Chrome\\User Data\\Wtsp'

    try:
        if option == 0:
            # If new QR code is requested. Clean up the profile directory.
            label.config(text=delete_chrome_profile(profile_path))

        CHROME_PROFILE_PATH = 'user-data-dir=' + profile_path

        options = webdriver.ChromeOptions()
        options.add_argument(CHROME_PROFILE_PATH)
        driver = webdriver.Chrome(options=options)

        # get config file info.
        config = load_config()
        csv_file = config["csv_file"]
        phone_row = config["phone_row"]
        message_file = "inputFiles/message.txt"

        # Gets message from the message file.
        message = open(message_file, 'r', encoding='utf-8').read()

        # Create empty list to store the phones that couldn't be reached.
        phones_that_failed = []

        # checks if the QR code was scanned
        if qrcode_auth(driver)["value"] != 0:
            label.config(text=qrcode_auth(driver)["text"])

        else:
            # start variables for counting messages sent and failed.
            success_count = 0
            failure_count = 0

            # start a loop that executes send_message() using al the csv contacts.
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)  # skip header row
                for row in reader:
                    phone = re.sub(r'\D', '', row[phone_row])
                    try:
                        if send_message(driver, phone, message, label) == 0:
                            success_count += 1
                            success_label.config(text="Messages Sent: " + str(success_count))
                        else:
                            phones_that_failed.append(phone)
                            failure_count += 1
                            failure_label.config(text="Failed: " + str(failure_count))
                    except Exception:
                        phones_that_failed.append(phone)
                        failure_count += 1
                        failure_label.config(text="Failed: " + str(failure_count))

        label.config(text="Finished sending the messages\n"
                          "You can close this window")

        log_failures(phones_that_failed)

        pb.destroy()

    except Exception as e:
        tk.messagebox.showerror("Error", f"Program Error:{e}\nPlease restart the app.")
        root.quit()


def load_frame1():
    frame1.tkraise()
    frame1.pack_propagate(False)
    # logo widgets
    logo_img = ImageTk.PhotoImage(file="assets/AutoZapLogo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    # instructions widget
    tk.Label(
        frame1,
        text="Ready to start sending messages?",
        bg=bg_color,
        fg="#EEEBDB",
        font=("Calibri", 14)
    ).pack(pady=20)

    # button widget
    tk.Button(
        frame1,
        text="SEND MESSAGES",
        font=("Calibri", 12, "bold"),
        bg="#EEEBDB",
        fg="#274245",
        cursor="hand2",
        activebackground="#274245",
        activeforeground="#EEEBDB",
        command=lambda: load_frame2()
    ).pack(ipadx=20)


def load_frame2():
    """Loads the second frame with two buttons. The button 'Scan New QR' evokes the load_frame3 with the parameter 0
    and the button 'Continue'  with the parameter 1"""
    frame2.tkraise()
    frame2.pack_propagate(False)

    # logo widgets
    logo_img = ImageTk.PhotoImage(file="assets/AutoZapLogo.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(
        frame2,
        text="Scan a new QR code or Continue?",
        bg=bg_color,
        fg="#EEEBDB",
        font=("Calibri", 14)
    ).pack(pady=20)

    tk.Button(
        frame2,
        text="NEW QR CODE",
        font=("Calibri", 12, "bold"),
        bg="#EEEBDB",
        fg="#274245",
        cursor="hand2",
        activebackground="#274245",
        activeforeground="#EEEBDB",
        command=lambda: load_frame3(0)
    ).pack(ipadx=20)

    tk.Button(
        frame2,
        text="CONTINUE",
        font=("Calibri", 12, "bold"),
        bg="#EEEBDB",
        fg="#274245",
        cursor="hand2",
        activebackground="#274245",
        activeforeground="#EEEBDB",
        command=lambda: load_frame3(1)
    ).pack(pady=20, ipadx=35, )


def load_frame3(option):
    frame3.tkraise()
    frame3.pack_propagate(False)

    # logo widgets
    logo_img = ImageTk.PhotoImage(file="assets/AutoZapBottom.png")
    logo_widget = tk.Label(frame3, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    label = tk.Label(
        frame3,
        text="AutoZap is sending your messages, please wait...",
        bg=bg_color,
        fg="#EEEBDB",
        font=("Calibri", 12))
    label.pack(pady=20)

    pb = ttk.Progressbar(
        frame3,
        orient='horizontal',
        length=200,
        mode='indeterminate'
    )
    pb.pack(pady=20)
    pb.start()

    success_label = tk.Label(
        frame3,
        text="Messages Sent:",
        bg=bg_color,
        fg="#EEEBDB",
        font=("Calibri bold", 14))
    success_label.pack(pady=10)

    failure_label = tk.Label(
        frame3,
        text="Failed:",
        bg=bg_color,
        fg="#EEEBDB",
        font=("Calibri bold", 14))
    failure_label.pack(pady=10)

    stop_button = tk.Button(
        frame3,
        text="EXIT",
        font=("Calibri", 12, "bold"),
        bg="#EEEBDB",
        fg="#274245",
        cursor="hand2",
        activebackground="#274245",
        activeforeground="#EEEBDB",
        command=lambda: root.quit()
    )
    stop_button.pack()

    threading.Thread(target=lambda: main(option, label, success_label, failure_label, pb)).start()


# initialize app
root = tk.Tk()
root.title("AutoZap for Chrome")
root.iconbitmap('assets/icon.ico')
bg_color = "#528E8F"

x = root.winfo_screenwidth() // 2
y = int(root.winfo_screenheight() * 0.1)
root.geometry('400x410+' + str(x) + '+' + str(y))

# create frame widgets
frame1 = tk.Frame(root, width=400, height=410, bg=bg_color)
frame2 = tk.Frame(root, width=400, height=410, bg=bg_color)
frame3 = tk.Frame(root, width=400, height=410, bg=bg_color)

for frame in (frame1, frame2, frame3):
    tk.Frame(root, width=400, height=410, bg=bg_color)
    frame.grid(row=0, column=0)

load_frame1()

# run app
root.mainloop()
