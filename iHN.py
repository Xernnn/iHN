import win32api
import win32con
import time
import cv2
import numpy as np
import pyautogui
import os
import re
import random
import pytesseract
from PIL import Image

COORDS = {
    'start_close': (1794, 808),
    'more': (1894, 811),
    'delete': (1715, 1022),
    'confirm_delete': (1509, 902),
    'tick_clone': (1246, 710),
    'batch': (1365, 623),
    'batch_clone': (1397, 681),
    'out': (1357, 477),
    'ihanoi': (1085, 418),
    
    'tai_khoan': (1136, 1004),
    'dki': (1050, 1006),
    'sdt': (747, 382),
    'tiep_tuc1': (963, 474),
    'otp': (237, 507),
    'nhap_sdt': (247, 271),
    'tiep_tuc2': (463, 348),
    'ma_moi': (455, 393),
    've_cu': (1000, 305),
    'tiep_tuc3': (959, 390),
    'ho_ten': (756, 310),
    'noi_o': (935, 396),
    'tim_kiem': (825, 484),
    'tx': (1204, 833),
    'nc': (1202, 719),
    'so_nha': (749, 452),
    'mat_khau': (742, 544),
    'nhap_lai': (751, 630),
    'hoan_tat': (962, 748),
}

# Set Tesseract path if it's not in PATH 
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

surnames = ["Nguyen", "Tran", "Le", "Pham", "Huynh", "Hoang", "Vu", "Vo", "Dang", "Bui", "Do", "Ho"]
middle_names = ["Van", "Thi", "Hong", "Ngoc", "Minh", "Quoc", "Duc", "Thanh", "Tan", "Xuan", "Anh", "Phuong"]
given_names = ["An", "Binh", "Cuong", "Duy", "Huong", "Lan", "Linh", "Mai", "Nam", "Phuc", "Quan", "Trang", "Tuan", "Vy", "Yen"]
street_names = [
    "Nguyen Xuan Linh",
    "Quan Nhan",
    "Nhan Hoa",
    "Le Van Luong",
    "Nguyen Tuan",
    "Nguy Nhu Kon Tum",
    "Giap Nhat"
]

account_counter = 1

def click(x, y):
    """Function to perform a quick click at specified coordinates"""
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def click_position(position_name):
    """Click at a predefined position by name"""
    if position_name in COORDS:
        x, y = COORDS[position_name]
        click(x, y)
        print(f"Clicked {position_name} at ({x}, {y})")
    else:
        print(f"Position {position_name} not found!")

def type_text(text):
    """Type text using pyautogui"""
    pyautogui.typewrite(text)
    time.sleep(0.1)

def check_screen(template_name, confidence=0.8):
    """Check if a specific image is present on screen"""
    template_path = os.path.join('images', template_name)
    try:
        location = pyautogui.locateOnScreen(template_path, confidence=confidence)
        return location is not None
    except Exception as e:
        print(f"Error checking screen: {e}")
        return False

def get_pixel_color(x, y):
    """Get RGB color of pixel at specified coordinates"""
    try:
        screenshot = pyautogui.screenshot()
        color = screenshot.getpixel((x, y))
        return color
    except Exception as e:
        print(f"Error getting pixel color: {e}")
        return None

def multiplayer_sequence():
    """Handle the multiplayer setup sequence with color check"""
    print("Starting multiplayer sequence...")
    
    click_position('start_close')
    time.sleep(0.2)
    click_position('confirm_delete')
    time.sleep(1)
    click_position('more')
    time.sleep(0.2)
    click_position('delete')
    time.sleep(0.2)
    click_position('confirm_delete')
    time.sleep(0.2)  # Wait for deletion to complete
    
    # # Check pixel color at (1769, 812)
    # color = get_pixel_color(1769, 812)
    # print(f"Detected color at check point: {color}")
    
    # if color == (102, 132, 255):  # If blue color detected
    #     print("Blue indicator detected - using short path")
    #     click_position('start_close')
    #     time.sleep(3)  # Wait for process to complete
    # else:
    #     print("Blue indicator not found - using long path")
    
    click_position('tick_clone')
    time.sleep(0.5)
    click_position('batch')
    time.sleep(0.5)
    click_position('batch_clone')
    time.sleep(4)
    click_position('start_close')
    time.sleep(12) 
    click_position('out')
    time.sleep(2) 
    click_position('ihanoi')
    time.sleep(2) 
    click_position('tai_khoan')
    time.sleep(1)

def generate_vietnamese_phone_number():
    """Generate a valid Vietnamese phone number starting with '09'"""
    return f"09{''.join([str(random.randint(0, 9)) for _ in range(8)])}"

def is_valid_vietnamese_phone_number(phone_number):
    """Validate Vietnamese phone number format"""
    pattern = r"^09\d{8}$"
    return bool(re.match(pattern, phone_number))

def enter_phone_number():
    """Generate and enter a valid phone number"""
    phone_number = generate_vietnamese_phone_number()
    print(f"Entering phone number: {phone_number}")
    return phone_number

def get_otp_from_screen():
    """
    Capture and extract OTP digits using Tesseract
    Focused on large, clear digits
    """
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            # Take screenshot of the OTP box region
            screenshot = pyautogui.screenshot(region=(200, 260, 500, 100))
            img = np.array(screenshot)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            
            # Adjust contrast based on attempt number
            alpha = 3.0 if attempt == 0 else (2.0 if attempt == 1 else 1.0)
            gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=0)
            
            # Aggressive thresholding
            _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            
            # Dilate to connect digit parts
            kernel = np.ones((2, 2), np.uint8)
            thresh = cv2.dilate(thresh, kernel, iterations=1)
            
            # Save debug image
            cv2.imwrite(f'otp_debug_attempt_{attempt + 1}.png', thresh)
            
            # Use Tesseract with specific config for digits only
            custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789 -c tessedit_char_blacklist=O'
            text = pytesseract.image_to_string(thresh, config=custom_config)
            
            # Clean up the result
            digits = ''.join(filter(str.isdigit, text))
            
            # If we have exactly 6 digits
            if len(digits) == 6:
                print(f"Found OTP: {digits}")
                return digits
            
            print(f"Attempt {attempt + 1}: Found {len(digits)} digits instead of 6: {digits}")
        
        except Exception as e:
            print(f"Error getting OTP on attempt {attempt + 1}: {e}")
    
    print("Failed to get a valid OTP after multiple attempts.")
    return None

def generate_vietnamese_name(min_words=2, max_words=3):
    """Generate a random Vietnamese name"""
    num_words = random.randint(min_words, max_words)
    name_parts = [random.choice(surnames)]
    
    if num_words > 2:
        middle_count = num_words - 2
        name_parts.extend(random.choices(middle_names, k=middle_count))
    
    name_parts.append(random.choice(given_names))
    return " ".join(name_parts)

def random_street_name():
    """Randomly select a street name from the list"""
    return random.choice(street_names)

def log_account(name, phone, address, success=True):
    """Log account information to a file"""
    global account_counter
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open('account_log.txt', 'a', encoding='utf-8') as f:
            if success:
                log_entry = f"[{timestamp}] Account {account_counter} - {name} - {phone} - {address}\n"
            else:
                log_entry = f"[{timestamp}] ERROR: OTP Failed for phone {phone}\n"
            
            # Also write to beginning of file
            with open('account_log.txt', 'r', encoding='utf-8') as original:
                content = original.read()
            with open('account_log.txt', 'w', encoding='utf-8') as modified:
                modified.write(log_entry + content)
                
        print(f"Logged: {log_entry.strip()}")
    except Exception as e:
        print(f"Error logging to file: {e}")

def check_blue_error(x, y, blue_range=(190, 200)):
    """Check if pixel at x,y has blue value in specified range"""
    try:
        screenshot = pyautogui.screenshot()
        color = screenshot.getpixel((x, y))
        # Check blue component (color[2] for RGB)
        return blue_range[0] <= color[2] <= blue_range[1]
    except Exception as e:
        print(f"Error checking color: {e}")
        return False

def ihanoi_sequence():
    global account_counter
    """Handle the iHanoi registration sequence"""
    print("Starting iHanoi registration sequence...")
    
    # Generate information early to log in case of failure
    phone_number = enter_phone_number()
    random_name = generate_vietnamese_name()
    address = random_street_name()
    
    click_position('dki')
    time.sleep(2.5)
    
    # Phone number registration
    click_position('sdt')
    time.sleep(0.5)
    
    print(phone_number)
    pyautogui.typewrite(phone_number)
    time.sleep(0.5)
    click_position('tiep_tuc1')
    time.sleep(0.5)
    
    # OTP handling
    click_position('ma_moi')
    time.sleep(2)
    click_position('nhap_sdt')
    time.sleep(0.5)
    pyautogui.typewrite(phone_number)
    time.sleep(0.5)
    click_position('tiep_tuc2')
    time.sleep(3)
    
    # Try to get OTP
    max_attempts = 8
    otp = None
    
    for attempt in range(max_attempts):
        otp = get_otp_from_screen()
        if otp and len(otp) == 6:
            print(f"Found OTP: {otp}")
            break
        print(f"OTP attempt {attempt + 1} failed, retrying...")
        time.sleep(1)
    
    if not otp:
        log_account(random_name, phone_number, address, success=False)
        print("Failed to get OTP, restarting from multiplayer sequence")
        return False

    # Continue with rest of sequence...
    click_position('ve_cu')
    time.sleep(0.5)
    pyautogui.typewrite(otp)
    time.sleep(0.5)
    click_position('tiep_tuc3')
    time.sleep(2.5)
    
    # Check for blue error indicator
    if check_blue_error(1180, 384):
        print("Detected error indicator (blue color), restarting from multiplayer")
        log_account(random_name, phone_number, address, success=False)
        return False
    
    # Personal information
    click_position('ho_ten')
    time.sleep(1)
    print(f"Using name: {random_name}")
    pyautogui.typewrite(random_name)
    time.sleep(1)
    
    click_position('noi_o')
    time.sleep(1)
    click_position('tim_kiem')
    time.sleep(1.3)
    pyautogui.typewrite('t')
    time.sleep(1.3)
    click_position('tx')
    time.sleep(2)
    click_position('nc')
    time.sleep(1.3)
    
    click_position('so_nha')
    time.sleep(1)
    print(f"Using address: {address}")
    pyautogui.typewrite(address)
    time.sleep(0.5)
    
    # Password
    click_position('mat_khau')
    time.sleep(0.5)
    pyautogui.typewrite("Thuongdinh@123")
    time.sleep(0.5)
    
    click_position('nhap_lai')
    time.sleep(0.5)
    pyautogui.typewrite("Thuongdinh@123")
    time.sleep(0.5)
    
    click_position('hoan_tat')
    time.sleep(3.5)
    
    account_counter += 1
    log_account(random_name, phone_number, address)  # Log successful account
    print(f"\nTotal accounts created: {account_counter}")
    return True

def main():
    global account_counter
    print("Program started. Press Ctrl+C to stop at any time.")
    try:
        while True:
            multiplayer_sequence()
            
            # Try first registration
            if not ihanoi_sequence():
                continue
                
            # Try second registration
            if not ihanoi_sequence():
                continue  
                
            # Try third registration
            if not ihanoi_sequence():
                continue  
            
    except KeyboardInterrupt:
        print(f"\nProgram stopped by user. Total accounts created: {account_counter}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print("Exiting program...")

if __name__ == "__main__":
    main()
