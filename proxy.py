import time
import redis
import grpc
from google.protobuf.timestamp_pb2 import Timestamp

import proxyTerminalCom_pb2
import proxyTerminalCom_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50060')

# create a stub (client)
stub = proxyTerminalCom_pb2_grpc.TerminalServiceStub(channel)

t_interval = 5
t_marge = 4
r = redis.Redis(host='localhost', port=6379, db=0)
while True:
    time_act = time.time_ns()
    time.sleep(t_interval)
    time_act = time_act + t_interval * 1000000000    # Millor calcular el temps actual sumant 5s al temps anterior pq time.sleep(5.0) no son exactament 5 segons i es podria quedar algun valor fora
    min_timestamp = time_act - (t_interval+t_marge) * 1000000000
    max_timestamp = time_act - t_marge * 1000000000 # Deixo 4 segons de marge pels valors que el sensor treu poc abans de començar a calcular la mitjana dels ultims 5s al proxy, per que el compute_server te un temps de calcul

    pattern = "m-*"
    print("------------------------------")
    print("Meteo:")
    n_values = 0
    wellness_mean = 0
    for key in r.scan_iter(match=pattern):
        # Extract the timestamp from the key
        key_timestamp = int(str(key).split("-")[1].replace("'", ""))
        # Check if the timestamp is within the last Y seconds
        if key_timestamp >= min_timestamp and key_timestamp < max_timestamp:
            # Get the value stored at the key
            wellness_data = r.get(key)
            wellness_data = float(str(wellness_data).split("'")[1].replace("'", ""))
            n_values = n_values + 1
            wellness_mean = wellness_mean + wellness_data
            print(str(key) + " " + str(r.get(key)))

    if n_values > 0:
        wellness_mean = wellness_mean/n_values
    print(wellness_mean)

    pattern = "p-*"
    print("Pollution:")
    n_values = 0
    pollution_mean = 0
    for key in r.scan_iter(match=pattern):
        # Extract the timestamp from the key
        key_timestamp = int(str(key).split("-")[1].replace("'", ""))
        # Check if the timestamp is within the last Y seconds
        if key_timestamp >= min_timestamp and key_timestamp < max_timestamp:
            # Get the value stored at the key
            pollution_data = r.get(key)
            pollution_data = float(str(pollution_data).split("'")[1].replace("'", ""))
            n_values = n_values + 1
            pollution_mean = pollution_mean + pollution_data
            print(str(key) + " " + str(r.get(key)))

    if n_values > 0:
        pollution_mean = pollution_mean/n_values
    print(pollution_mean)

    timestamp = Timestamp()
    timestamp.FromNanoseconds(max_timestamp) # Aqui en lloc d'agafar el temps maxim fins on es tracten les dades, potser s'hauria d'agafar el temps de la dada mes recent dins les que es tracten?
    coefficients = proxyTerminalCom_pb2.Coefficients(wellness_mean=wellness_mean, pollution_mean=pollution_mean, timestamp=timestamp)
    stub.send_results(coefficients)