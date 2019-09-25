import pyaudio
import wave
import json
import urllib3
import requests
import numpy as np
import socket


# UDP config:
UDP_IP = "localhost"
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
# VAD variables:
noise = 0
voice = 0
# Sound parameters:
laughter_id = 0
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
# Configure HTTP requests:
http = urllib3.PoolManager()
url = 'https://api.webempath.net/v2/analyzeWav'
api = "bGgzUd80q853LlOHoqZyWYnrSimSqRCwg6XaYqmfY2Y"
# Parse data from UDP port:
def data_parsing(data):
    # Split the data by the newlines:
    data = data.split('\n')
    # Remove blank spaces for every data:
    for i in range(data.__len__()):
        data[i] = data[i].strip()
    return data


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
            'apikey': "bGgzUd80q853LlOHoqZyWYnrSimSqRCwg6XaYqmfY2Y",
            "wav": ('stream.wav', file_data)
        }
    )
    # Deal with server response:
    if (res.status == 200):
        result = json.loads(res.data.decode('utf-8'))
        return result
    else:
        print("ERROR")

def save_laughter():
    global laughter_id
    laughter_id += 1
    laughter_path = "./wav_files/laughter_" + str(laughter_id) + ".wav"
    wf = wave.open(laughter_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
if __name__ == "__main__":
    while True:
        # xml_data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        # xml_data = xml_data.decode("utf-8")
        # data = data_parsing(xml_data)
        # for d in data:
        #     if "noise" in d:
        #         noise = float(''.join([c for c in d if c in '1234567890.']))
        #     elif "voice" in d:
        #         voice = float(''.join([c for c in d if c in '1234567890.']))
        # print(voice, noise)
        # if voice > noise:
        recording()
        data = webempath_request()
        # Processing the result:
        print("Anger:", data["anger"])
        print("Joy:", data["joy"])
        print("Calm:", data["calm"])
        print("Sorrow:", data["sorrow"])
        print("Engergy:", data["energy"])
        # Detect joy recording:
        if data["joy"] >= 15:
           save_laughter()
        # Reset the frame for next recording:
        frames = []

