#!/bin/bash

terminal_names=("redis-server" "terminal" "proxy" "compute_server" "load_balancer" "air_sensor" "pollution_sensor")

commands=("redis-server" "python3 terminal.py" "python3 proxy.py" "python3 compute_server.py" "python3 load_balancer.py" "python3 air_sensor.py" "python3 pollution_sensor.py")

n_exec=(1 2 1 1 1 2 2)

for i in {0..6}
do
    terminal_name=${terminal_names[$i]}
    command=${commands[$i]}
    for (( j=0; j<${n_exec[$i]}; j++ ))
    do
        if [ "$terminal_name" = "terminal" ]; then
            command="${commands[$i]} $j"
        fi
        gnome-terminal --tab --working-directory=$(dirname -- "$(readlink -f -- "$0")";) -- bash -c "printf '\033]0;%s\007' '$terminal_name'; $command; exec bash"
    done
    sleep 0.1
done