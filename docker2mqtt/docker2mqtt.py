import paho.mqtt.client as mqtt
import subprocess
import time
from subprocess import PIPE

from secret import mqttuser
from secret import mqttpass
from secret import mqtturl
from secret import dockerssh

client = mqtt.Client("docker")

client.username_pw_set(mqttuser,mqttpass)
client.connect(mqtturl)

containers = ["tsukihi"]
states = [""]
payload = "{"

while True:
	output=subprocess.run(["ssh", dockerssh, '''docker ps -a --format "{{.Names}};{{.Status}}"'''],stdout=PIPE,stderr=PIPE)
	# output=subprocess.run(["ssh", dockerssh, '''docker ps -a --format "{{.Names}};{{.Status}}"'''],capture_output=True)
	if output.returncode == 0:
		if states[0]!="Up":
			states[0]="Up"
			payload+='"'+containers[0]+'":"Up"'
		for line in output.stdout.decode("utf-8").splitlines():
			name, rawstate = line.split(";",1)
			state = rawstate.split(" ",1)[0]
			if state!="Up":
				state="Down"
			try:
				index=containers.index(name)
			except ValueError:
				containers.append(name)
				states.append(state)
				payload+='"'+name+'":"'+state+'",'
			else:
				if states[index]!=state:
					states[index]=state
					payload+='"'+name+'":"'+state+'",'
	else:
		if states[0]=="Up":
			for i in range(len(states)):
				payload+='"'+containers[i]+'":"Down",'
				states[i]="Down"
	if payload!="{":
		client.publish("docker2mqtt/StateChanged",payload[:-1]+"}")
		# print(payload[:-1]+"}")
		payload="{"
	time.sleep(60)