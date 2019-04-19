import paho.mqtt.client as mqttClient
import time
import json

Connected = False #global variable for the state of the connection
broker_address= "10.42.12.200"
port = 1883

publicScore = [0,0]

speeds = [0,0,0,0,0,0,0,0,0,0]
distance = [0,0,0,0,0,0,0,0,0,0]

client = mqttClient.Client()

def main():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address, port=port)
    client.loop_start()
    
    for i in range(0, 10):
        client.subscribe([("TeamFitness/player"+ str(i) +"/speed", 2)])
        client.subscribe([("TeamFitness/player"+ str(i) +"/distance", 2)])
    
    while Connected != True:    #Wait for connection
        print("waiting")
        time.sleep(0.1)
    
    try:
        while True:
            publishArrAvg("distance", distance)
            time.sleep(0.5)
 
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        
def publishArrAvg(topic, arr):
    avg = 0
    for val in arr:
        avg += val
    print(avg)
    client.publish("TeamFitness/public/"+ topic, avg, qos=2, retain = True)
    
def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    player = int(message.topic[18])
    
    topic = message.topic.split('/')[-1]
    
    if(topic == "distance"):
        distance[player] = data
    if(topic == "speed"):
        0==0 #replace later
    #print("Player " + str(player) + "'s " + topic + " is: " + str(data))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
        
main()
