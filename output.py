from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import math

import paho.mqtt.client as mqttClient
#settings for mqtt connection

Connected = False #global variable for the state of the connection
broker_address= "10.42.12.200"
port = 1883
client = mqttClient.Client() #global client variable
    
from time import sleep
from signal import pause


def connectClient():
    #client.username_pw_set(user, password=password)
    client.on_connect = on_connect
    client.connect(broker_address, port=port)
    client.loop_start()
    
    client.subscribe([("TeamFitness/public/speed", 2)])
    client.subscribe([("TeamFitness/public/distance", 2)])

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
        
connectClient()

publicScores = [0,0]
def on_message(client, userdata, message):
    print("msg")
    data = json.loads(message.payload.decode())
    if(message.topic == "TeamFitness/public/distance"):
        publicScores[1] = data

shared_list =  [0,0]

#def getValues(in_queue, shared_list):
def getValues():
    sense = SenseHat()

    gravity = [0, 0, 0]
    linear_acceleration = [0, 0, 0]

    distance = 0
    while(True):
        acc= sense.get_gyroscope_raw()
        accelerometer_values = [acc['x'], acc['y'], acc['z']]
        kFilteringFactor = 0.6
        
        global shared_list
        
        gravity[0] = (accelerometer_values[0] * kFilteringFactor) + (gravity[0] * (1.0 - kFilteringFactor));
        gravity[1] = (accelerometer_values[1] * kFilteringFactor) + (gravity[1] * (1.0 - kFilteringFactor));
        gravity[2] = (accelerometer_values[2] * kFilteringFactor) + (gravity[2] * (1.0 - kFilteringFactor));

        linear_acceleration[0] = (accelerometer_values[0] - gravity[0]);
        linear_acceleration[1] = (accelerometer_values[1] - gravity[1]);
        linear_acceleration[2] = (accelerometer_values[2] - gravity[2]);

        magnitude = 0.0;
        magnitude = math.sqrt(linear_acceleration[0]*linear_acceleration[0]+linear_acceleration[1]*linear_acceleration[1]+linear_acceleration[2]*linear_acceleration[2]);
        magnitude = abs(magnitude);
        
        speed = 0
        if(magnitude > 0.3):
            speed = ((magnitude - 0.3)*(1/(1-0.3)))*0.9+1
        
        distance += speed
        
        publishValue("speed", speed)
        publishValue("distance", distance)
        shared_list = [speed, distance]
        
        #print("Speed, distance", shared_list)
        sleep(0.5)
        
        
        #--------------------------- send to server code goes here
        
        

lastPos = [0,0]

posit = [0,1]

users = [[255,0,0],
         [0,255,0],
         [0,0,255],
         [255,255,0],
         [0,255,255],
         [255,0,255],
         [255,255,255],
         [122,255,122],
         [255,122,255],
         [122,255,122],
        ]

def publishValue(what, val):
    client.publish("TeamFitness/player"+ str(posit[1]) +"/" + what, val, qos=2, retain = False)


sense = SenseHat()

def writeNum():
    sense.show_letter(str(posit[1])[0], text_colour=users[posit[1]])

def writeWord(wrd):
    sense.show_message(str(wrd), scroll_speed=0.05, text_colour=users[posit[1]])
    
def writeSteps():
    sense.show_message(str(round(shared_list[0], 2)), scroll_speed=0.05, text_colour=users[posit[1]])

def writeSpeed():
    print(shared_list)
    sense.show_message(str(round(shared_list[1], 2)), scroll_speed=0.05, text_colour=users[posit[1]])

def getPublicScoreDistance():
    writeWord(publicScores[1])
    
def displayText():
    writeWord("doing well!")
    

infoFuncs = {0 : writeNum, 1 : writeSteps, 2 : writeSpeed, 3 : getPublicScoreDistance}

#this bit does a thing
def displayInformation(n):
    infoFuncs[n]()

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def loop(value, min_value=0, max_value=7):
    if(value > max_value):
        return min_value
    elif(value < min_value):
        return max_value
    return value

def pushed_up(event):
    if event.action != ACTION_RELEASED:
        posit[0] = clamp(posit[0] - 1, 0, len(infoFuncs)-1)

def pushed_down(event):
    if event.action != ACTION_RELEASED:
        posit[0] = clamp(posit[0] + 1, 0, len(infoFuncs)-1)

def pushed_left(event):
    if event.action != ACTION_RELEASED:
        posit[1] = loop(posit[1] - 1, 0, len(users)-1)

def pushed_right(event):
    if event.action != ACTION_RELEASED:
        posit[1] = loop(posit[1] + 1, 0, len(users)-1)

    
def refresh():
    global lastPos
    global posit
        
    if(posit != lastPos):
        lastPos = posit.copy()
        sense.clear()
        displayInformation(posit[0])
        
sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
sense.stick.direction_any = refresh

refresh()
getValues()
#pause()