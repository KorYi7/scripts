#!/bin/bash
if ! [ -p "/tmp/vmpipe" ]; then
	mkfifo -m 0600 "/tmp/vmpipe"
fi

~/.config/polybar/vm-status.sh &

if [ -e "/tmp/.vmlock" ]; then
	rm "/tmp/.vmlock"
fi

while true; do
	MYVAR=$(<"/tmp/vmpipe")
	echo $MYVAR
done