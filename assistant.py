import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import re

# --- 1. CONFIGURATION ---
# vvv PASTE YOUR KEY BELOW vvv
GOOGLE_API_KEY = "PASTE_YOUR_REAL_LONG_KEY_HERE" 
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. SETUP BRAIN ---
model = genai.GenerativeModel(
    'gemini-flash-latest',
    system_instruction="You are a helpful assistant. Reply in a short, clear manner."
)

# --- 3. SETUP MOUTH ---
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    clean_text = re.sub(r'[^\w\s,!.?]', '', text)
    print(f"🤖 AI: {clean_text}")
    engine.say(clean_text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    
    # We removed the specific ID. Now it uses the System Default.
    with sr.Microphone() as source:
        print("\n🎤 Listening... (Speak now!)")
        
        # This makes it more sensitive to your voice
        r.energy_threshold = 300 
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = r.listen(source, timeout=5)
            print("Thinking... 🤔")
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

# --- MAIN LOOP ---
if __name__ == "__main__":
    speak("System online.")
    
    while True:
        user_input = listen()
        if user_input:
            try:
                response = model.generate_content(user_input)
                speak(response.text)
            except Exception as e:
                speak("I have a headache.")