import vosk
import pyaudio
import json
import os

# Set the model path (use an absolute path)
model_path = "C:/Users/hegde/OneDrive/Desktop/speechToText by Python/vosk-model-en-us-0.42-gigaspeech"

# Check if the model path exists and contains the necessary files
if not os.path.exists(model_path):
    raise Exception(f"Model path '{model_path}' does not exist.")
if not os.path.isdir(model_path):
    raise Exception(f"'{model_path}' is not a directory.")
if not os.path.isfile(os.path.join(model_path, "model.conf")):
    raise Exception(f"Model directory '{model_path}' does not contain 'model.conf' file.")

# Initialize the model with model_path
model = vosk.Model(model_path)

# Create a recognizer
rec = vosk.KaldiRecognizer(model, 16000) # sample rate = 16000

# Open the microphone stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)

# Specify the path for the output text file
output_file_path = "recognized_text.txt"

# Open a text file in write mode using a 'with' block
with open(output_file_path, "w") as output_file:
    print("Listening for speech. Say 'Terminate' to stop.")
    # Start streaming and recognize speech
    while True:
        data = stream.read(4096) # read in chunks of 4096 bytes
        if rec.AcceptWaveform(data): # accept waveform of input voice
            # Parse the JSON result and get the recognized text
            result = json.loads(rec.Result())
            recognized_text = result['text']
            
            # Write recognized text to the file
            output_file.write(recognized_text + "\n")
            print(recognized_text)
            
            # Check for the termination keyword
            if "terminate" in recognized_text.lower():
                print("Termination keyword detected. Stopping...")
                break

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio object
p.terminate()
