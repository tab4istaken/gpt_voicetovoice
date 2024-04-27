import speech_recognition as sr
import datetime
import whisper
import edge_tts
import os
import sounddevice as sd
import soundfile as sf
import re
import openai
import asyncio

api_key = "" #replace with your own OpenAI API key
conversation_history = [{"role": "system", "content": "You're a friendly assistant."}] #change the "content" to your starting prompt

model = whisper.load_model("small")
recognizer = sr.Recognizer()
microphone = sr.Microphone()
#this uses your default microphone
voice = ""
openai.api_key = api_key
headers = {"Content-Type": "application/json"}
async def communicate(TEXT, VOICE, OUTPUT_FILE):
    communicate = edge_tts.Communicate(TEXT, VOICE, rate="+25%")
    await communicate.save(OUTPUT_FILE)
output_file = "last_output.wav"
print("Ready for input.")
recording_counter = 1
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"recorded_audio_{timestamp}_{recording_counter}.wav"

def record_audio_continuously():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio_data = recognizer.listen(source, timeout=5)
                print(file_name)
                with open(file_name, "wb") as file:
                    file.write(audio_data.get_wav_data())
                audio = whisper.load_audio(file_name)
                audio = whisper.pad_or_trim(audio)
                mel = whisper.log_mel_spectrogram(audio).to(model.device)
                _, probs = model.detect_language(mel)
                language = f"{max(probs, key=probs.get)}"
                if language == "en":
                    voice = "en-US-AriaNeural"
                elif language == "ja":
                    voice = "ja-JP-NanamiNeural"
                else:
                    voice = "en-US-AriaNeural"
                #more languages are supported using the edge-tts voices
                options = whisper.DecodingOptions()
                result = whisper.decode(model, mel, options)
                print("User:", result.text)
                os.remove(file_name)
                conversation_history.append({"role": "user", "content": result.text})
                try:
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo", #you can use any GPT model
                        messages=conversation_history,
                        temperature=1.1,
                        max_tokens=128
                    )
                    reply = response.choices[0].message.content
                except openai.RateLimitError:
                    print("Error! You have exceeded your OpenAI quota. Make sure you have enough credit for this operation.")
                    reply = "OpenAI rate limit error"
                    #exit() - if you don't want the voice to say that you're out of credit 
                conversation_history.append({"role": "assistant", "content": reply})
                loop = asyncio.get_event_loop_policy().get_event_loop()
                loop.run_until_complete(communicate(reply, voice, output_file))
                #use this for RVC / to change audio source (use sd.query_devices() to figure out the right device):
                #sd.default.device = 12
                data, fs = sf.read("last_output.wav", dtype = 'float32')
                sd.play(data,fs)
                sd.wait()
                os.remove("last_output.wav")
            except sr.WaitTimeoutError:
                pass

while True:
    try:
        record_audio_continuously()
    except KeyboardInterrupt:
        print("\nProgram closed.")
        exit()
