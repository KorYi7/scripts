#!/usr/bin/python3
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
client.loop_start()

containers = ["tsukihi"]
states = [""]
payload = "{"
changed = True

while True:
	output=subprocess.run(["ssh", dockerssh, '''docker ps -a --format "{{.Names}};{{.Status}}"'''],stdout=PIPE,stderr=PIPE)
	# output=subprocess.run(["ssh", dockerssh, '''docker ps -a --format "{{.Names}};{{.Status}}"'''],capture_output=True)
	if output.returncode == 0:
		if states[0]!="Up":
			states[0]="Up"
			changed=True
			# payload+='"'+containers[0]+'":"Up",'
		for line in output.stdout.decode("utf-8").splitlines():
			name, rawstate = line.split(";",1)
			state = rawstate.split(" ",1)[0]
			if state!="Up":
				state="Down"
			try:
				index=containers.index(name.replace("-","_"))
			except ValueError:
				containers.append(name.replace("-","_"))
				states.append(state)
				changed=True
				# payload+='"'+name+'":"'+state+'",'
			else:
				if states[index]!=state:
					states[index]=state
					changed=True
					# payload+='"'+name+'":"'+state+'",'
	else:
		if states[0]=="Up":
			for i in range(len(states)):
				changed=True
				# payload+='"'+containers[i]+'":"Down",'
				states[i]="Down"
	if changed:
		for j in range(len(states)):
				payload+='"'+containers[j]+'":"'+states[j]+'",'
		err=client.publish("docker2mqtt/StateChanged",payload[:-1]+"}")
		if err.rc==mqtt.MQTT_ERR_NO_CONN:
			client.reconnect()
			client.publish("docker2mqtt/StateChanged",payload[:-1]+"}")
		changed=False
		# print(payload[:-1]+"}")
		payload="{"
	time.sleep(45)