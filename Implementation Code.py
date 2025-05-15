import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
LED_PIN = 17  # Example device control pin
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Command mappings
COMMANDS = {
    "turn on the light": LED_PIN,
    "light on": LED_PIN,
    "turn off the light": LED_PIN,
    "light off": LED_PIN,
    "switch the light": LED_PIN
}

def listen_for_command():
    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def process_command(command):
    if command in COMMANDS:
        pin = COMMANDS[command]
        current_state = GPIO.input(pin)
        
        if "on" in command or ("switch" in command and not current_state):
            GPIO.output(pin, GPIO.HIGH)
            print("Device turned ON")
        elif "off" in command or ("switch" in command and current_state):
            GPIO.output(pin, GPIO.LOW)
            print("Device turned OFF")
    else:
        print("Command not recognized")

def main():
    try:
        while True:
            command = listen_for_command()
            if command:
                process_command(command)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()