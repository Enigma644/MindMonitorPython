"""
Mind Monitor - EEG OSC Receiver
Coded: James Clutterbuck (2022)
Requires: pip install python-osc
"""
from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server

ip = "0.0.0.0"
port = 5000
filePath = 'OSC-Python-Recording.csv'
auxCount = -1
recording = False

f = open (filePath,'w+')

def writeFileHeader():
    global auxCount
    fileString = 'TimeStamp,RAW_TP9,RAW_AF7,RAW_AF8,RAW_TP10,'
    for x in range(0,auxCount):
        fileString += 'AUX'+str(x+1)+','
    fileString +='Marker\n'
    f.write(fileString)

def eeg_handler(address: str,*args):
    global recording
    global auxCount
    if auxCount==-1:
        auxCount = len(args)-4
        writeFileHeader()
    if recording:
        timestampStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        fileString = timestampStr
        for arg in args:
            fileString += ","+str(arg)            
        fileString+="\n"
        f.write(fileString)
    
def marker_handler(address: str,i):
    global recording
    global auxCount
    timestampStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    markerNum = address[-1]
    if recording:
        fileString = timestampStr+',,,,,'
        for x in range (0,auxCount):
            fileString +=','
        fileString +='/Marker/'+markerNum+"\n"
        f.write(fileString)
    if (markerNum=="1"):        
        recording = True
        print("Recording Started.")
    if (markerNum=="2"):
        f.close()
        recording = False
        server.shutdown()
        print("Recording Stopped.")    

if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/eeg", eeg_handler)
    dispatcher.map("/Marker/*", marker_handler)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port "+str(port)+"\nSend Marker 1 to Start recording and Marker 2 to Stop Recording.")
    server.serve_forever()