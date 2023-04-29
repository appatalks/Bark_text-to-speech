# Python to run Suno-ai's Text-to-Speech API - BARK.

# Thank you for the idea and intial code to play with @
# https://github.com/suno-ai/bark/pull/84

import datetime
from bark import SAMPLE_RATE,generate_audio,preload_models
from scipy.io.wavfile import write as write_wav
import numpy as np
import nltk
from loguru import logger
import playsound


# Set up loguru logger
logger.add("/tmp/bark.log", format="{message}")

# nltk.download('punkt')
preload_models()

# Set up sample rate (importing instead atm)
# SAMPLE_RATE = 22050

# Set a History Prompt (buggy)
HISTORY_PROMPT = "en_speaker_3"

while True:
    # Prompt input
    initial_prompt = "WOMAN: " + input(""" Input: """)
    long_string = initial_prompt

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
    filename = f"Bark_audio_{timestamp_str}.wav"
    write_wav(filename, SAMPLE_RATE, combined_audio)

    # play audio using playsound
    playsound.playsound(filename)
