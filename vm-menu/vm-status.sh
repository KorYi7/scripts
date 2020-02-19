#!/bin/bash
if ! [ -p "/tmp/vmpipe" ]; then
  mkfifo -m 0600 "/tmp/vmpipe"
fi

if [ "$1" == "-s" ]; then
	if [ ! -e /tmp/.vmlock ]; then
		OUTPUT=$(virsh -c qemu:///system domstate win10)
		OUTPUT2=$(echo -n $OUTPUT)
		if [ "$OUTPUT2" = "shut off" ]
		then
		    echo "%{A3:Windows:}$OUTPUT2%{A}" > "/tmp/vmpipe"
		else
			echo "%{A3:W-menu:}$OUTPUT2%{A}" > "/tmp/vmpipe"
		fi
	fi
	exit
fi

while true; do
	if [ ! -e /tmp/.vmlock ]; then
		OUTPUT=$(virsh -c qemu:///system domstate win10)
		OUTPUT2=$(echo -n $OUTPUT)
		if [ "$OUTPUT2" = "shut off" ]
		then
		    echo "%{A3:Windows:}$OUTPUT2%{A}" > "/tmp/vmpipe"
		else
		    echo "%{A3:W-menu:}$OUTPUT2%{A}" > "/tmp/vmpipe"
		fi
		sleep 10
	fi
done
