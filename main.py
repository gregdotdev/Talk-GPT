import speech_recognition as sr
import g4f
import re
import pyttsx3

def remove_source(text):
    cleaned_text = re.sub(r'\[Source \d+\]\(https:\/\/.+?\)', '', text)
    return cleaned_text

def get_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Something:")
        audio = r.listen(source)
    try:
        user_text = r.recognize_google(audio, language='en-US')
        print(user_text)
        return user_text
    except sr.UnknownValueError:
        print("Sorry, i didn't understand the audio.")
        return None
    except sr.RequestError as e:
        print("Error at fetch results; {0}".format(e))
        return None

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    user_text = get_user_input()
    if user_text:
        model_response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": user_text}],
            provider=g4f.Provider.You
        )
        
        model_response_str = str(model_response)
        
        response = remove_source(model_response_str)
        print("Response:", response)
        
        speak(response)

if __name__ == "__main__":
    main()
