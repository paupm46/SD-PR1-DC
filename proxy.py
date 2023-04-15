import time
import redis
import grpc
from google.protobuf.timestamp_pb2 import Timestamp

import proxyTerminalCom_pb2
import proxyTerminalCom_pb2_grpc

# Crear conexiones gRPC con los terminales
nCS = 2 # Número de terminales creados
stubs = []
for x in range(nCS):
    port = 50060 + x
    port = str(port)
    channel = grpc.insecure_channel('localhost:'+port)
    stub = proxyTerminalCom_pb2_grpc.TerminalServiceStub(channel)
    stubs.append(stub)


r = redis.Redis(host='localhost', port=6379, db=0)
t_interval = 5
t_marge = 4
time.sleep(5) # Esperar 5 segundos para que se calculen algunos datos
time_act = time.time_ns()
while True:
    time.sleep(t_interval)
    time_act = time_act + t_interval * 1000000000    # Mejor calcular el tiempo actual sumando 5s en el tiempo anterior pq time.sleep(5.0) no son exactamente 5 segundos y se podría quedar algún valor fuera
    min_timestamp = time_act - (t_interval+t_marge) * 1000000000
    max_timestamp = time_act - t_marge * 1000000000 # Dejo 4 segundos de margen por los valores que el sensor quita poco antes de empezar a calcular la media de los últimos 5s en el proxy, para que el compute_server tiene un tiempo de cálculo

    pattern = "m-*" # Obtener las claves de los valores de meteo
    n_values = 0
    wellness_mean = 0
    for key in r.scan_iter(match=pattern):
        # Extraer timestamp de la clave
        key_timestamp = int(str(key).split("-")[1].replace("'", ""))
        # Comprovar si el timestamp esta dentro del rango a calcular la mediana
        if key_timestamp >= min_timestamp and key_timestamp < max_timestamp:
            # Obtener valor almacenado en la clave
            wellness_data = r.get(key)
            wellness_data = float(str(wellness_data).split("'")[1].replace("'", ""))
            n_values = n_values + 1
            wellness_mean = wellness_mean + wellness_data
            r.delete(key)

    if n_values > 0:
        wellness_mean = wellness_mean/n_values # Calcular mediana de wellness (meteo)

    pattern = "p-*" # Obtener las claves de los valores de pollution
    n_values = 0
    pollution_mean = 0
    for key in r.scan_iter(match=pattern):
        # Extraer timestamp de la clave
        key_timestamp = int(str(key).split("-")[1].replace("'", ""))
        # Comprovar si el timestamp esta dentro del rango a calcular la mediana
        if key_timestamp >= min_timestamp and key_timestamp < max_timestamp:
            # Obtener valor almacenado en la clave
            pollution_data = r.get(key)
            pollution_data = float(str(pollution_data).split("'")[1].replace("'", ""))
            n_values = n_values + 1
            pollution_mean = pollution_mean + pollution_data
            r.delete(key)

    if n_values > 0:
        pollution_mean = pollution_mean/n_values # Calcular mediana de pollution

    timestamp = Timestamp()
    timestamp.FromNanoseconds(max_timestamp) # Crear timestamp con el mas reciente del rango
    coefficients = proxyTerminalCom_pb2.Coefficients(wellness_mean=wellness_mean, pollution_mean=pollution_mean, timestamp=timestamp)
    for x in range(nCS):
        stubs[x].send_results(coefficients) # Enviar coeficientes a todos los terminales
