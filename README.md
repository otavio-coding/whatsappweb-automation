# WhatsApp Bulk Message Sender

This Python script automates sending bulk messages on WhatsApp using Selenium. It requires a CSV file with contact numbers and sends a predefined message to each contact. Below are the details and instructions for using the script.

## Requirements
- Python 3
- Google Chrome browser
- Appropriate version of [ChromeDriver](https://sites.google.com/chromium.org/driver/)

## Instructions

1. **Install Dependencies:**
    ```bash
    pip install selenium
    ```

2. **Download ChromeDriver:**
    Download the appropriate version of [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatible with your Google Chrome browser version. Ensure that the Chromedriver executable is in your system's PATH.

3. **Define CSV File:**
    Replace `'ContactList.csv'` with the path to your CSV file containing contact numbers.

4. **Define Message:**
    Edit the `message.txt` file with the message you want to send.

5. **Run the Script:**
    Execute the script:
    ```bash
    python main.py
    ```

6. **QR Code Authentication:**
    The script opens the WhatsApp web page, and if QR scanning is required, it waits for the user to scan the QR code.

7. **Sending Messages:**
    The script reads the CSV file, extracts phone numbers, and sends the predefined message to each contact. Any failed attempts are recorded.

8. **Finish:**
    After sending messages, the script prints the phones that failed to receive the message.

## Important Notes
- Ensure Chromedriver version is compatible with your Chrome browser version.
- The script depends on a CSV file structure with phone numbers in the specified column.
- Customize the message and CSV file paths according to your needs.

Happy messaging! 🚀📱
