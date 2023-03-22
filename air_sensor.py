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
    meteo_data = detector.analyze_air()
    timestamp = Timestamp()
    timestamp.GetCurrentTime()
    data = sensorLBCom_pb2.RawMeteoData(id='Air Sensor', temperature=meteo_data['temperature'], humidity=meteo_data['humidity'], timestamp=timestamp)
    stub.send_meteo_data(data)
    #print(meteo_data)
