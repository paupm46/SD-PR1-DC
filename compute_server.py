import grpc
from concurrent import futures
import time
from meteo_utils import MeteoDataProcessor
import redis

# import the generated classes
import LBComputeServerCom_pb2
import LBComputeServerCom_pb2_grpc


class MeteoData:
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity


class PollutionData:
    def __init__(self, co2):
        self.co2 = co2


processor = MeteoDataProcessor()

r = redis.Redis(host='localhost', port=6379, db=0)


class ComputeServerServicer(LBComputeServerCom_pb2_grpc.ComputeServerServiceServicer):

    def process_meteo_data(self, meteo_data, context): # Procedimiento llamado por el load balancer
        wellness_data = processor.process_meteo_data(MeteoData(meteo_data.temperature, meteo_data.humidity)) # Procesar meteo data del air sensor
        r.set("m-"+str(meteo_data.timestamp.ToNanoseconds()), str(wellness_data)) # Guardar valor obtenido con la clave m-timestamp en Redis
        response = LBComputeServerCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def process_pollution_data(self, pollution_data, context): # Procedimiento llamado por el load balancer
        p_data = processor.process_pollution_data(PollutionData(pollution_data.co2)) # Procesar pollution data del pollution sensor
        r.set("p-" + str(pollution_data.timestamp.ToNanoseconds()), str(p_data)) # Guardar valor obtenido con la clave p-timestamp en Redis
        response = LBComputeServerCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

# Crear servidores gRPC
nCS = 3 # Número de compute servers a crear
servers = []
for x in range(nCS):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servers.append(server)
    LBComputeServerCom_pb2_grpc.add_ComputeServerServiceServicer_to_server(ComputeServerServicer(), servers[x])
    port = 50052 + x
    port = str(port)
    print('Starting server. Listening on port '+port+'.')
    servers[x].add_insecure_port('0.0.0.0:'+port)
    servers[x].start()


# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    r.close()
    for x in range(nCS):
        servers[x].stop(0)