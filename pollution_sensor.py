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
    pollution_data = detector.analyze_pollution()
    timestamp = Timestamp()
    timestamp.FromNanoseconds(time.time_ns())
    data = sensorLBCom_pb2.RawPollutionData(id='Pollution Sensor', co2=pollution_data['co2'], timestamp=timestamp)
    stub.send_pollution_data(data)
    #print(data)