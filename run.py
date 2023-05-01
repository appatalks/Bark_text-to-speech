# Python to run Suno-ai's Text-to-Speech API - BARK.

# Thank you for the token counter idea and intial code to play with @
# https://github.com/suno-ai/bark/pull/84

import datetime
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import numpy as np
import nltk
from http.server import HTTPServer, BaseHTTPRequestHandler

# nltk.download('punkt')
preload_models()

# Set up sample rate (importing instead atm)
# SAMPLE_RATE = 22050

# Set a History Prompt (buggy)
HISTORY_PROMPT = "en_speaker_3"

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Add these lines to allow cross-origin requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        # Get the user input from the request body
        content_length = int(self.headers['Content-Length'])
        user_input = self.rfile.read(content_length).decode('utf-8')

        long_string = user_input

        # Tokenize to split strink into chunks for processing
        sentences = nltk.sent_tokenize(long_string)

        chunks = ['']
        token_counter = 0

        for sentence in sentences:
            current_tokens = len(nltk.Text(sentence))
            if token_counter + current_tokens <= 250:
                token_counter = token_counter + current_tokens
                chunks[-1] = chunks[-1] + " " + sentence
            else:
                chunks.append(sentence)
                token_counter = current_tokens

        # Generate audio for each prompt
        audio_arrays = []
        for prompt in chunks:
            audio_array = generate_audio(prompt,history_prompt=HISTORY_PROMPT)
            # audio_array = generate_audio(prompt)
            audio_arrays.append(audio_array)

        # Combine the audio files
        combined_audio = np.concatenate(audio_arrays)

        # Write the combined audio to a file
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # filename = f"Bark_audio_{timestamp_str}.wav"
        filename = './audio/bark_audio.wav'
        write_wav(filename, SAMPLE_RATE, combined_audio)

        # play audio using playsound
        # playsound.playsound(filename)

        # Send a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        # self.send_header('Content-type', 'audio/wav')
        self.end_headers()
        # self.wfile.write(b'String sent to Bark\n')
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.end_headers()

def do_GET(self):
    # Check the path of the request
    if self.path == '/':
        # Return the index.html page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('index.html', 'rb') as f:
            self.wfile.write(f.read())
    elif self.path == '/audio':
        # Return the audio file
        self.send_response(200)
        self.send_header('Content-type', 'audio/wav')
        self.end_headers()
        with open('./audio/bark_audio.wav', 'rb') as f:
            self.wfile.write(f.read())
    else:
        # Return a 404 error
        self.send_error(404, 'File Not Found')


# Start the HTTP server
httpd = HTTPServer(('localhost', 8080), RequestHandler)
httpd.serve_forever()
