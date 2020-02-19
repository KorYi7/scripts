#!/bin/bash
if [ -e "/tmp/.vmlock" ]; then
	rm /tmp/.vmlock
	~/.config/polybar/vm-status.sh -s
else
	touch /tmp/.vmlock

	if ! [ -p "/tmp/vmpipe" ]; then
		mkfifo -m 0600 "/tmp/vmpipe"
	fi

	echo "%{A:Wshutdown:}%{u#ffb347 +u}Shutdown%{-u}%{A} %{A:Wdestroy:}%{u#ff6961 +u}Force off%{-u}%{A} %{A:Wfreset:}%{u#ff6961 +u}Reset%{-u}%{A} %{A:W-menu:}%{u#4BA6B3 +u}Cancel%{-u}%{A}" > "/tmp/vmpipe"
fi