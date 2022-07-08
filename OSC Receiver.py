"""
Mind Monitor - EEG OSC Receiver
Coded: James Clutterbuck (2021)
Requires: pip install python-osc
"""
from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server

ip = "0.0.0.0"
port = 5000
filePath = 'OSC-Python-Recording.csv'
recording = False
f = open (filePath,'w+')
f.write('TimeStamp,RAW_TP9,RAW_AF7,RAW_AF8,RAW_TP10,AUX,Marker\n')
# Muse S with 2 AUX Channels:
# f.write('TimeStamp,RAW_TP9,RAW_AF7,RAW_AF8,RAW_TP10,AUX_R,AUX_L,Marker\n')

def eeg_handler(address: str,*args):
    global recording
    if recording:
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
        f.write(timestampStr)
        for arg in args:
            f.write(","+str(arg))
        f.write("\n")
    
def marker_handler(address: str,i):
    global recording
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    markerNum = address[-1]
    f.write(timestampStr+",,,,,,/Marker/"+markerNum+"\n")
    # Muse S with 2 AUX Channels:
    # f.write(timestampStr+",,,,,,,/Marker/"+markerNum+"\n")
    if (markerNum=="1"):        
        recording = True
        print("Recording Started.")
    if (markerNum=="2"):
        f.close()
        server.shutdown()
        print("Recording Stopped.")    

if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/eeg", eeg_handler)
    dispatcher.map("/Marker/*", marker_handler)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port "+str(port)+"\nSend Marker 1 to Start recording and Marker 2 to Stop Recording.")
    server.serve_forever()
