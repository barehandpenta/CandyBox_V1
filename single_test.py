import pyaudio
import wave
import json
import urllib3



file = open("wav_files/laugh_10_mono.wav", 'rb')
file_data = file.read()
http = urllib3.PoolManager()
res = http.request(
    method='POST',
    url='https://api.webempath.net/v2/analyzeWav',
    fields={
        'apikey': "R_LMDXRxQFRTpECYEKD7MAyNJgwTxnbcgkIDFORhmVI",
        "wav": ('stream.wav', file_data)
    }
)

if(res.status == 200):
    result = json.loads(res.data.decode('utf-8'))
    print(result)
else:
    print("ERROR")

