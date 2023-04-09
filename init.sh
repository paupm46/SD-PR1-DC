#!/bin/bash

terminal_names=("redis-server" "terminal" "proxy" "compute_server" "load_balancer" "air_sensor" "pollution_sensor")

commands=("redis-server" "python3 terminal.py" "python3 proxy.py" "python3 compute_server.py" "python3 load_balancer.py" "python3 air_sensor.py" "python3 pollution_sensor.py")


for i in {0..6}
do
    terminal_name=${terminal_names[$i]}
    command=${commands[$i]}
    gnome-terminal --working-directory=/home/milax/PycharmProjects/SD-PR1/ -- bash -c "printf '\033]0;%s\007' '$terminal_name'; $command; exec bash"
    sleep 5
done
