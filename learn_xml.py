import xml.etree.ElementTree as ET
import re

data = '''<?xml version="1.0" ?>
<vad>
    <noise>0.953545</noise>
    <voice>0.046455</voice>
    <male>0.000000</male>
    <female>0.000000</female>
    <laugh>0.000000</laugh>
</vad>'''

data = data.split('\n')

noise = 0
voice = 0
male = 0
female = 0
laugh = 0

for i in range(data.__len__()):
    data[i] = data[i].strip()

for d in data:
    if "noise" in d:
        noise = ''.join([c for c in d if c in '1234567890.'])
    elif "voice" in d:
        voice = ''.join([c for c in d if c in '1234567890.'])
    elif "male" in d:
        male = ''.join([c for c in d if c in '1234567890.'])
    elif "female" in d:
        female = ''.join([c for c in d if c in '1234567890.'])
    elif "laugh" in d:
        laugh = ''.join([c for c in d if c in '1234567890.'])

print("Noise: " + str(noise))
print("Voice: " + str(voice))
print("Male: " + str(male))
print("Female: " + str(female))
print("Laugh: " + str(laugh))





