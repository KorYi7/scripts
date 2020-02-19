#!/bin/bash

# Specifying the icon(s) in the script
# This allows us to change its appearance conditionally

#icon=""
if pgrep "spotify" > /dev/null
then #spotify running
    player_status=$(playerctl -p spotify status 2> /dev/null)
    if [[ $? -eq 0 ]]; then
        metadata="$(playerctl -p spotify metadata artist) - $(playerctl -p spotify metadata title)"
    fi

    # Foreground color formatting tags are optional
    if [[ $player_status = "Playing" ]]; then
        echo "${metadata:0:75}"       # Orange when playing
    elif [[ $player_status = "Paused" ]]; then
        echo "%{F#888888}[paused]${metadata:0:75}"       # Greyed out info when paused
    else
        echo "%{F#888888}Stopped"                 # Greyed out icon when stopped
    fi
else 
    echo "%{F#888888}No player running"
#    metadata=$(mpc current)
#    status=$(mpc | awk 'match($0, /\[.*\]/) { print substr($0, RSTART, RLENGTH) }')
#    if [[ $status = "[playing]" ]]; then
#        echo "$metadata"
#    elif [[ $status = "[paused]" ]]; then
#        echo "%{F#888888}[paused]${metadata:1:5}"
#    else
#        echo "%{F#888888}Stopped"
#    fi
fi
