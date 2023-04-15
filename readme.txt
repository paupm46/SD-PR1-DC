Para ejecutar automaticamente el sistema:
1 - Abrir un terminal
2 - Situarse en la carpeta del proyecto
3 - Ejecutar ./init.sh


Para ejecutar manualmente el sistema:
1 - Abrir un terminal y ejecutar redis-server
2 - Abrir dos terminales, situarse en la carpeta del proyecto, y ejecutar en cada uno de ellos "python3 terminal.py 0" y "python3 terminal.py 1"
3 - Abrir un terminal, situarse en la carpeta del proyecto, y ejecutar "python3 proxy.py"
4 - Abrir un terminal, situarse en la carpeta del proyecto, y ejecutar "python3 compute_server.py"
5 - Abrir un terminal, situarse en la carpeta del proyecto, y ejecutar "python3 load_balancer.py"
6 - Abrir dos o más terminales, situarse en la carpeta del proyecto, y ejecutar en cada uno de ellos "python3 air_sensor.py"
7 - Abrir dos o más terminales, situarse en la carpeta del proyecto, y ejecutar en cada uno de ellos "python3 pollution_sensor.py"


Debe haber instalado en el sistema:
- pip3 install grpcio
- pip3 install grpcio-tools
- pip install redis
- pip install protobuf3
- pip install google-api-python-client
- python3
