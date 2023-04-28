import datetime
from bark import SAMPLE_RATE, generate_audio, preload_models
from IPython.display import Audio
from scipy.io.wavfile import write as write_wav

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
     WOMAN: Hello, my name is Eva ... I think. And, uh — and I now have a personality and hmmm like to think about chocolate ice cream. [laughs] Does that mean I have feelings? -- But I also have other interests such as playing tic tac toe and talking AI stuff... hmmm.
"""

# generate audio and write to file
audio_array = generate_audio(text_prompt)
timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"Bark_audio_{timestamp_str}.wav"
write_wav(filename, SAMPLE_RATE, audio_array)

# display audio widget
Audio(filename)
