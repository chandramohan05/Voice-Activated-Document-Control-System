import speech_recognition as sr
import pyautogui
import pyaudio
import re
from word2number import w2n

def get_microphone_index():
    p = pyaudio.PyAudio()
    bluetooth_mic_index = None
    default_mic_index = None

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info.get('name').lower()
        if 'bluetooth' in device_name or 'headset' in device_name:
            bluetooth_mic_index = i
            break
        elif default_mic_index is None and 'input' in device_name:
            default_mic_index = i

    p.terminate()
    return bluetooth_mic_index if bluetooth_mic_index is not None else default_mic_index

def scroll_screen(direction, pages):
    scroll_amount_per_page = 500  # Adjust this value based on the typical page size in your application
    total_scroll_amount = pages * scroll_amount_per_page

    # Perform the scroll in steps to ensure large scroll amounts are handled
    step_size = 500  # This is an arbitrary step size for each scroll operation, adjust as needed
    if direction == "up":
        for _ in range(0, total_scroll_amount, step_size):
            pyautogui.scroll(step_size)  # Scroll up
    elif direction == "down":
        for _ in range(0, total_scroll_amount, step_size):
            pyautogui.scroll(-step_size)  # Scroll down

def scroll_scree(direction, pages):
    scroll_amount_per_page = 1000  # Adjust this value based on the typical page size in your application
    total_scroll_amount = pages * scroll_amount_per_page

    # Perform the scroll in steps to ensure large scroll amounts are handled
    step_size = 5000  # This is an arbitrary step size for each scroll operation, adjust as needed
    if direction == "up":
        for _ in range(0, total_scroll_amount, step_size):
            pyautogui.scroll(step_size)  # Scroll up
    elif direction == "down":
        for _ in range(0, total_scroll_amount, step_size):
            pyautogui.scroll(-step_size)  # Scroll down


def recognize_speech(mic_index=None):
    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=mic_index) as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")

        try:
            audio_data = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            print("Processing...")

            text = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text}")

            match = re.search(r'scroll (\d+|one|two|three|four|five|six|seven|eight|nine|ten) pages? (up|down)', text.lower())
            if match:
                number_word = match.group(1)
                pages = w2n.word_to_num(number_word) if number_word.isalpha() else int(number_word)
                direction = match.group(2)
                scroll_scree(direction, pages)
            elif "scroll up" in text.lower():
                scroll_screen("up", 1)
            elif "scroll down" in text.lower():
                scroll_screen("down", 1)
            elif "exit" in text.lower():
                print("Exiting the program.")
                return False
            else:
                print("Command not recognized. Please say 'scroll up', 'scroll down', or 'scroll <n> pages up/down', or 'exit'.")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
    return True

if __name__ == "__main__":
    mic_index = get_microphone_index()
    print(f"Using microphone index: {mic_index}")

    while True:
        if not recognize_speech(mic_index):
            break
