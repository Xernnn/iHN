import pyautogui
import time

# Fail-safe feature: Moving mouse to upper-left corner will stop the script
pyautogui.FAILSAFE = True

# Get the screen size
screen_width, screen_height = pyautogui.size()
print(f"Screen size: {screen_width}x{screen_height}")
print("Mouse Tracker Started! Move mouse to upper-left corner to stop.")
print("Press Ctrl+C in terminal to exit.")

try:
    while True:
        # Get current mouse position
        pyautogui.displayMousePosition()
        x, y = pyautogui.position()
        
        # Ensure coordinates are within screen bounds
        x = min(max(0, x), screen_width)
        y = min(max(0, y), screen_height)
        
        # Clear the previous line and print the current position
        print(f"\rMouse Position: x={x:4d}, y={y:4d}", end="")
        
        # Small delay to prevent high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nMouse Tracker Stopped!") 