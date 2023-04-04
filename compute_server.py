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

    def process_meteo_data(self, meteo_data, context):
        #print(meteo_data)
        wellness_data = processor.process_meteo_data(MeteoData(meteo_data.temperature, meteo_data.humidity))
        print(wellness_data)
        print(meteo_data.timestamp.ToNanoseconds())
        r.set("m-"+str(meteo_data.timestamp.ToNanoseconds()), str(wellness_data))
        #value = r.get("m-"+str(meteo_data.timestamp.ToNanoseconds()))
        #print(value)
        response = LBComputeServerCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def process_pollution_data(self, pollution_data, context):
        #print(pollution_data)
        p_data = processor.process_pollution_data(PollutionData(pollution_data.co2))
        print(pollution_data.timestamp.ToNanoseconds())
        print(p_data)
        r.set("p-" + str(pollution_data.timestamp.ToNanoseconds()), str(p_data))
        response = LBComputeServerCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

"""
# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_LBServiceServicer_to_server`
# to add the defined class to the server
LBComputeServerCom_pb2_grpc.add_ComputeServerServiceServicer_to_server(ComputeServerServicer(), server)

# listen on port 50052
print('Starting server. Listening on port 50052.')
server.add_insecure_port('0.0.0.0:50052')
server.start()


# create a gRPC server
server2 = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_LBServiceServicer_to_server`
# to add the defined class to the server
LBComputeServerCom_pb2_grpc.add_ComputeServerServiceServicer_to_server(ComputeServerServicer(), server2)

# listen on port 50053
print('Starting server. Listening on port 50053.')
server2.add_insecure_port('0.0.0.0:50053')
server2.start()
"""

nCS = 3
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