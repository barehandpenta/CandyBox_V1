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
seconds = 2
frames = []  # Initialize array to store audio frames
p = pyaudio.PyAudio()  # Create an interface to PortAudio
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)


http = urllib3.PoolManager()
url = 'https://api.webempath.net/v2/analyzeWav'
api = "R_LMDXRxQFRTpECYEKD7MAyNJgwTxnbcgkIDFORhmVI"


# Function for audio recording to wav file:
def recording():
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
    # Write to temporary file:
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
# Function to use the wav file above for request to the WebEmpath API:
def webempath_request():
    file = open("stream.wav", 'rb') #Open the recorded audio
    file_data = file.read()
    # Make HTTP request:
    res = http.request(
        method='POST',
        url='https://api.webempath.net/v2/analyzeWav',
        fields={
            'apikey': "R_LMDXRxQFRTpECYEKD7MAyNJgwTxnbcgkIDFORhmVI",
            "wav": ('stream.wav', file_data)
        }
    )
    # Deal with server response:
    if (res.status == 200):
        result = json.loads(res.data.decode('utf-8'))
        return result
    else:
        print("ERROR")

# if __name__ == "__main__":
while True:
    recording()
    result = webempath_request()
    # Reset the frame for next recording:
    frames = []
    #
    print(result)
