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
        print(meteo_data)
        wellness_data = processor.process_meteo_data(MeteoData(meteo_data.temperature, meteo_data.humidity))
        print(wellness_data)
        r.set(str(meteo_data.timestamp), str(wellness_data))
        value = r.get(str(meteo_data.timestamp))
        print(value)
        response = LBComputeServerCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def process_pollution_data(self, pollution_data, context):
        print(pollution_data)
        pollution_data = processor.process_pollution_data(PollutionData(pollution_data.co2))
        print(pollution_data)
        response = LBComputeServerCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_LBServiceServicer_to_server`
# to add the defined class to the server
LBComputeServerCom_pb2_grpc.add_ComputeServerServiceServicer_to_server(ComputeServerServicer(), server)

# listen on port 50052
print('Starting server. Listening on port 50052.')
server.add_insecure_port('0.0.0.0:50052')
server.start()

"""
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

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    r.close()
    server.stop(0)