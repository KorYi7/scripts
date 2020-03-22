import paho.mqtt.client as mqtt
import subprocess
import time
from subprocess import PIPE
from secret import mqttuser
from secret import mqttpass
from secret import mqtturl
from secret import dockerssh

# client = mqtt.Client("docker")

# client.username_pw_set(mqttuser,mqttpass)
# client.connect(mqtturl)
# client.publish("test","ON")

containers = ["tsukihi"]
states = [""]
while True:
	output=subprocess.run(["ssh", dockerssh, '''docker ps -a --format "{{.Names}};{{.Status}}"'''],stdout=PIPE,stderr=PIPE)
	# output=subprocess.run(["ssh", dockerssh, '''docker ps -a --format "{{.Names}};{{.Status}}"'''],capture_output=True)
	if output.returncode == 0:
		if states[0]!="Up":
			states[0]="Up"
			# client.publish(containers[0],states[0])
			print(containers[0],states[0])
		for line in output.stdout.decode("utf-8").splitlines():
			name, rawstate = line.split(";",1)
			state = rawstate.split(" ",1)[0]
			try:
				index=containers.index(name)
			except ValueError:
				containers.append(name)
				states.append(state)
				# client.publish(name,state)
				print(name,state)
			else:
				if states[index]!=state:
					states[index]=state
					# client.publish(name,state)
					print(name,state)
	else:
		if states[0]=="Up":
			states[0]="Down"
			# client.publish(containers[0],states[0])
			print(containers[0],states[0])
	time.sleep(10)