from meteo_utils import MeteoDataDetector
import time
import grpc
from google.protobuf.timestamp_pb2 import Timestamp

# import the generated classes
import sensorLBCom_pb2
import sensorLBCom_pb2_grpc

detector = MeteoDataDetector()

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = sensorLBCom_pb2_grpc.LBServiceStub(channel)

while True:
    time.sleep(1.0)
    pollution_data = detector.analyze_pollution() # Generar dato de polución
    timestamp = Timestamp()
    timestamp.FromNanoseconds(time.time_ns()) # Crear timestamp actual
    data = sensorLBCom_pb2.RawPollutionData(id='Pollution Sensor', co2=pollution_data['co2'], timestamp=timestamp) # Crear parámetro gRPC
    stub.send_pollution_data(data) # Enviar datos a load balancer
