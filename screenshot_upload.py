import serial
import time
import pyautogui
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import ImageGrab  # For screen capture

# === CONFIGURATION ===
FORM_URL = 'https://tally.so/r/wANV40'
SCREENSHOT_PATH = 'C:\\Users\\User\\Desktop\\automation\\HNS project\\screenshot\\screenshot.png'  # Adjust as per your system
SERIAL_PORT = 'COM5'  # Update if your Arduino uses a different port

# XPaths for form elements
DATETIME_INPUT_XPATH = '//*[@id="734fed5a-bb9c-4e34-ae43-955c6fd5dd45"]'
FILE_INPUT_XPATH = '//*[@id="__next"]/div/main/section/form/div[1]/div[5]/div/div/input'
SUBMIT_BUTTON_XPATH = '//*[@id="__next"]/div/main/section/form/div[2]/div[1]/button'

# === FUNCTIONS ===
def capture_screen():
    img = ImageGrab.grab()
    img.save(SCREENSHOT_PATH)
    print(f"[INFO] Screenshot saved to {SCREENSHOT_PATH}")

def upload_screenshot():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    print("[INFO] Opening Tally form...")
    driver.get(FORM_URL)
    time.sleep(5)

    # Fill date & time field
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datetime_input = driver.find_element(By.XPATH, DATETIME_INPUT_XPATH)
    datetime_input.send_keys(now)
    print(f"[INFO] Entered date & time: {now}")
    time.sleep(1)

    # Upload Screenshot
    file_input = driver.find_element(By.XPATH, FILE_INPUT_XPATH)
    file_input.send_keys(SCREENSHOT_PATH)
    print("[INFO] Screenshot uploaded.")
    time.sleep(5)  # Wait for file to register

    # Submit Form
    submit_btn = driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH)
    submit_btn.click()
    print("[INFO] Form submitted successfully.")
    
    time.sleep(3)
    driver.quit()

# === MAIN LISTENER ===
print("[INFO] Listening for PIR sensor signal...")

ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
time.sleep(2)  # Wait for serial connection to establish

while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        print(f"[SERIAL] Received: {line}")
        
        if "Person Detected" in line:
            print("[TRIGGER] Person detected! Capturing and uploading...")
            capture_screen()
            upload_screenshot()
            print("[INFO] Process complete. Waiting for next signal...\n")
