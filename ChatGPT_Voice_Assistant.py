import openai
import pyttsx3
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = "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"
# Initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except: 
        print("Unknown Error")

def generate_response(prompt):
    response = openai.Completion.create (
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1000,
        n= 1,
        stop = None,
        temperature = 0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

conversation_history = []

def main():
    # Wait for the user to say "Bob"
    print("Say 'Bob' to start recording your question... ")
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)

        try: 
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "bob":

                while True:
                    print("Say your question...")
                    with sr.Microphone() as source: 
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open("input.wav", "wb") as f:
                            f.write(audio.get_wav_data())

                        # Transcribe audio to text
                        text = transcribe_audio_to_text("input.wav")
                        if text:
                            print(f"You said: {text}")
                            prompt = "\n".join(conversation_history) + "\nYou said: " + text
                            response = generate_response(prompt)
                            print(f"Bob says: {response}")
                            conversation_history.append("You said: " + text)
                            conversation_history.append("Bob says: " + response)

                            speak_text(response)
                            if text.lower() == "bye":
                                break
        except Exception as e:
            print("An error occurred: {}".format(e))
                    
if __name__ == "__main__":
    main()