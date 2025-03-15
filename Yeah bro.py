import pyautogui
import random
import time

# Function to simulate realistic typing (random delay between keystrokes)
def realistic_typing(text):
    for char in text:
        pyautogui.write(char)
        # Random delay between 0.05 and 0.15 seconds for more realism
        time.sleep(random.uniform(0.05, 0.15))

# Function to simulate mouse movements (e.g., moving to another file or window)
def realistic_mouse_movement():
    # Move the mouse to a random position on the screen
    pyautogui.moveTo(random.randint(100, 2000), random.randint(100, 1000), duration=random.uniform(0.5, 1.5))

    # Click the mouse at the new location
    pyautogui.click()

    # Optional: Add a pause to mimic reading or thinking
    time.sleep(random.uniform(2, 5))

# Main function to simulate a fake coding session
def simulate_fake_coding():
    # Start by opening a new file or editor (in real-life usage, you'd automate that step too)
    time.sleep(2)  # Wait for a moment to simulate opening a text editor

    # Simulate typing some code
    code = """
def fake_function():
    # This is a fake function to simulate coding
    print("Hello, world!")
    
fake_function()
"""
    
    # Simulate typing the code with realistic delays
    realistic_typing(code)

    # Simulate some mouse movements to mimic the real workflow (e.g., switching between files)
    realistic_mouse_movement()

    # Add more realistic typing with pauses
    realistic_typing("\n# Adding comments to fake the code review process")
    
    # Another mouse movement to simulate user interaction with the IDE or editor
    realistic_mouse_movement()

    # Add a final section of typing to "finish" the work
    realistic_typing("\n# Final code submission\nprint('Code completed!')")

    # Simulate a long pause as if the user is reviewing or waiting for a response
    time.sleep(random.uniform(5, 10))

# Final code submission
print('Code completed!') 
# Run the simulation
simulate_fake_coding()

            