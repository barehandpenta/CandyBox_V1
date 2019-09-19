import pyaudio
import wave
import json
import urllib3
import requests
import numpy as np


# Sound parameters:
filename = "stream.wav"
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 11025  # Record at 44100 samples per second
seconds = 4
p = pyaudio.PyAudio()  # Create an interface to PortAudio
http = urllib3.PoolManager()
url = 'https://api.webempath.net/v2/analyzeWav'
api = "R_LMDXRxQFRTpECYEKD7MAyNJgwTxnbcgkIDFORhmVI"

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

while True:
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    # Store data in chunks for 3 second:
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        # np_data = np.frombuffer(data, dtype=np.int16)
        frames.append(data)
    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    file = open("stream.wav", 'rb')
    file_data = file.read()

    res = http.request(
        method='POST',
        url='https://api.webempath.net/v2/analyzeWav',
        fields={
            'apikey': "R_LMDXRxQFRTpECYEKD7MAyNJgwTxnbcgkIDFORhmVI",
            "wav": ('stream.wav', file_data)
        }
    )

    if(res.status== 200):
        result = json.loads(res.data.decode('utf-8'))
        print(result)
        # emo = []
        # emo.append(result['calm'])
        # emo.append(result['anger'])
        # emo.append(result[' joy'])
        # emo.append(result['sorrow'])
        # emo.append(result['energy'])
    else:
        print("ERROR")
    frames = []
