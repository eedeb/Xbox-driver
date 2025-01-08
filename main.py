import pyautogui
from inputs import get_gamepad
import threading
import time
import speech_recognition as sr
recognizer = sr.Recognizer()


# Sensitivity factors for controlling mouse speed
SENSITIVITY_X = 30
SENSITIVITY_Y = 30
SCROLL_SENSITIVITY = 20  # Default sensitivity for scrolling
FAST_SCROLL_SENSITIVITY = 100  # Sensitivity for faster scrolling when R3 is pressed
DEAD_ZONE = 5000

# Variables to store joystick and trigger input
x_movement = 0
y_movement = 0
left_trigger = 0
right_trigger = 0
is_left_joystick_pressed = False  # Flag to track if the left joystick is pressed
right_joystick_y = 0  # To store vertical movement of the right joystick
is_right_joystick_pressed = False  # Flag to track if the right joystick is pressed

# Custom functions for button actions
def left_click():
    pyautogui.click()
    print("Left click triggered!")

def right_click():
    pyautogui.rightClick()
    print("Right click triggered!")

def trigger_action():
    print(f"Trigger action: LT={left_trigger}, RT={right_trigger}")
    if right_trigger > 250:
        pyautogui.hotkey('ctrl', 'tab')
    elif left_trigger > 250:
        pyautogui.hotkey('ctrl', 'shift', 'tab')

def left_joystick():
    global SENSITIVITY_X, SENSITIVITY_Y, is_left_joystick_pressed
    if is_left_joystick_pressed:
        # Increase sensitivity to 100 when joystick is pressed
        SENSITIVITY_X = 100
        SENSITIVITY_Y = 100
        print(f"Sensitivity set to 100 while L3 is pressed")
    else:
        # Revert sensitivity to 20 when joystick is released
        SENSITIVITY_X = 20
        SENSITIVITY_Y = 20
        print(f"Sensitivity set to 20")

def custom_function():
    pyautogui.hotkey('win', 'r')
def close_function():
    pyautogui.hotkey('ctrl', 'w')
def enter_key():
    pyautogui.press('enter')
def backspace():
    pyautogui.press('backspace')
def right_arrow():
    pyautogui.press('right')
def left_arrow():
    pyautogui.press('left')
def spacebar():
    pyautogui.press('space')
def text_speak():
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
            var = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service: {e}")
    pyautogui.write(var)
# Function to process gamepad input
def process_gamepad():
    global x_movement, y_movement, left_trigger, right_trigger, is_left_joystick_pressed, right_joystick_y, is_right_joystick_pressed
    print("Listening for controller input... Press Ctrl+C to quit.")
    try:
        while True:
            events = get_gamepad()
            for event in events:
                # Detect joystick axis movements
                if event.ev_type == "Absolute":
                    if event.code == "ABS_X":  # Left joystick X-axis
                        x_movement = event.state if abs(event.state) > DEAD_ZONE else 0

                    elif event.code == "ABS_Y":  # Left joystick Y-axis
                        y_movement = -event.state if abs(event.state) > DEAD_ZONE else 0

                    elif event.code == "ABS_Z":  # Left trigger (LT)
                        left_trigger = event.state
                        trigger_action()

                    elif event.code == "ABS_RZ":  # Right trigger (RT)
                        right_trigger = event.state
                        trigger_action()

                    elif event.code == "ABS_RX":  # Right joystick X-axis (left-right movement, not used)
                        pass

                    elif event.code == "ABS_RY":  # Right joystick Y-axis (up-down movement)
                        right_joystick_y = event.state
                    # D-pad
                    # Handle D-pad horizontal movement
                    if event.code == "ABS_HAT0X":
                        if event.state == -1:  # D-pad left
                            backspace()
                        elif event.state == 1:  # D-pad right
                            enter_key()

                    # Handle D-pad vertical movement
                    elif event.code == "ABS_HAT0Y":
                        if event.state == -1:  # D-pad up
                            spacebar()
                        elif event.state == 1:  # D-pad down
                            custom_function()
                # Detect button presses
                elif event.ev_type == "Key":
                    if event.code == "BTN_SOUTH":  # A button
                        if event.state == 1:  # Button pressed
                            left_click()

                    elif event.code == "BTN_EAST":  # B button
                        if event.state == 1:  # Button pressed
                            right_click()

                    elif event.code == "BTN_NORTH":  # X button
                        if event.state == 1:  # Button pressed
                            text_speak()
                    elif event.code == "BTN_WEST":  # X button
                        if event.state == 1:  # Button pressed
                            close_function()

                    # Detect L3 press and release
                    if event.code == "BTN_THUMBL":
                        if event.state == 1:  # Left joystick press (L3)
                            is_left_joystick_pressed = True
                            left_joystick()
                        elif event.state == 0:  # Left joystick release (L3)
                            is_left_joystick_pressed = False
                            left_joystick()

                    # Detect R3 press and release (Right joystick button press)
                    if event.code == "BTN_THUMBR":
                        if event.state == 1:  # Right joystick press (R3)
                            is_right_joystick_pressed = True
                        elif event.state == 0:  # Right joystick release (R3)
                            is_right_joystick_pressed = False

                    if event.code == "BTN_TL":  # Left bumper (LB / L1)
                        if event.state == 1:  # Button pressed
                            left_arrow()

                    elif event.code == "BTN_TR":  # Right bumper (RB / R1)
                        if event.state == 1:  # Button pressed
                            right_arrow()

    except KeyboardInterrupt:
        print("\nExiting...")

# Function to move the mouse smoothly based on joystick input
def move_mouse():
    global SENSITIVITY_X
    global SENSITIVITY_Y
    global x_movement, y_movement
    while True:
        # Scale joystick input and apply sensitivity
        dx = (x_movement / 32768) * SENSITIVITY_X
        dy = (y_movement / 32768) * SENSITIVITY_Y

        # Move the mouse gradually
        pyautogui.moveRel(dx, dy, duration=0.1)

        # Add a small delay for smoother movement

# Function to scroll the page based on right joystick Y-axis input
def scroll_page():
    global right_joystick_y, is_right_joystick_pressed
    while True:
        # Set the scroll sensitivity based on whether the right joystick is pressed
        scroll_sensitivity = FAST_SCROLL_SENSITIVITY if is_right_joystick_pressed else SCROLL_SENSITIVITY

        # If the right joystick is moved up or down
        if abs(right_joystick_y) > DEAD_ZONE:
            if right_joystick_y > 0:  # Moving up (positive Y value)
                pyautogui.scroll(scroll_sensitivity)
            elif right_joystick_y < 0:  # Moving down (negative Y value)
                pyautogui.scroll(-scroll_sensitivity)

        time.sleep(0.01)

# Start the gamepad processing in a separate thread
gamepad_thread = threading.Thread(target=process_gamepad)
gamepad_thread.daemon = True
gamepad_thread.start()

# Start the mouse movement loop
move_mouse_thread = threading.Thread(target=move_mouse)
move_mouse_thread.daemon = True
move_mouse_thread.start()

# Start the scrolling loop
scroll_page_thread = threading.Thread(target=scroll_page)
scroll_page_thread.daemon = True
scroll_page_thread.start()

# Keep the program running
while True:
    time.sleep(10)
