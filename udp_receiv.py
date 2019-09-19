import socket
import serial
import time

arduino = serial.Serial('COM1', baudrate = 115200, timeout=1)

UDP_IP = "localhost"
UDP_PORT = 1234

# STATE: NEUTRAI, TALKING and LAUGHING

state = 'NEUTRAI'
last_state = 'NEUTRAI'

speed = 70


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def data_parsing(data):
    # Split the data by the newlines:
    data = data.split('\n')
    # Remove blank spaces for every data:
    for i in range(data.__len__()):
        data[i] = data[i].strip()
    return data
noise = 0
voice = 0
male = 0
female = 0
laugh = 0
interval = 0

while True:
    xml_data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    xml_data = xml_data.decode("utf-8")
    data = data_parsing(xml_data)
    for d in data:
        if "noise" in d:
            noise = float(''.join([c for c in d if c in '1234567890.']))
        elif "voice" in d:
            voice = float(''.join([c for c in d if c in '1234567890.']))
        elif "male" in d:
            male = float(''.join([c for c in d if c in '1234567890.']))
        elif "female" in d:
            female = float(''.join([c for c in d if c in '1234567890.']))
        elif "laugh" in d:
            laugh = float(''.join([c for c in d if c in '1234567890.']))

    # print("Noise: " + str(noise))
    # print("Voice: " + str(voice))
    # print("Male: " + str(male))
    # print("Female: " + str(female))
    # print("Laugh: " + str(laugh))
    # print("\n")

    if noise > voice:
        state = 'NEUTRAL'
    elif voice > noise:
        if laugh < 0.5:
            state = 'TALKING'
        elif laugh > 0.5:
            state = 'LAUGHING'

    # state checking:
    if state != last_state:
        if(state == 'TALKING'):

            if time.time() - interval > 5:
                interval = time.time()
                arduino.write(b'F|5')

        elif(state == 'NEUTRAL'):
            arduino.write(b'Pause!')
            interval = time.time()

    last_state = state
