import paho.mqtt.client as mqtt
import subprocess
import os

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("label/print")

def on_message(client, userdata, msg):
    text = msg.payload.decode()
    print("Print message: " + text);
    subprocess.run(["convert", "-size", "300x70", "xc:none", "-gravity", "Center",
                    "-pointsize", "35", "-annotate", "0",
                    f"{text}", "result.png"])
    os.system('python3.9 label_maker.py CHANGETODEVICEMACADDRESS --image result.png')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("username", "password")
client.connect("host", 1883, 60)

client.loop_forever()