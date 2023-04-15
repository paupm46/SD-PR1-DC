import grpc
from concurrent import futures
import time
from datetime import datetime

# import the generated classes
import sensorLBCom_pb2
import sensorLBCom_pb2_grpc

# import the generated classes
import LBComputeServerCom_pb2
import LBComputeServerCom_pb2_grpc

# Crear conexiones gRPC con los compute servers
nCS = 3 # Número de compute servers creados
stubs = []
for x in range(nCS):
    port = 50052 + x
    port = str(port)
    channel = grpc.insecure_channel('localhost:'+port)
    stub = LBComputeServerCom_pb2_grpc.ComputeServerServiceStub(channel)
    stubs.append(stub)


class LoadBalancerServicer(sensorLBCom_pb2_grpc.LBServiceServicer):
    i = 0 # Contador modulo nServers que se va incrementando cada vez que llega un dato y sirve de índice para seleccionar el compute server al que asignar la tarea

    def send_meteo_data(self, meteo_data, context): # Procedimiento llamado por un air sensor
        self.i = (self.i + 1) % nCS # Seleccionar el compute server al que asignar la tarea
        stubs[self.i].process_meteo_data.future(meteo_data) # Enviar dato a procesar al compute server seleccionado
        response = sensorLBCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def send_pollution_data(self, pollution_data, context): # Procedimiento llamado por un pollution sensor
        self.i = (self.i + 1) % nCS # Seleccionar el compute server al que asignar la tarea
        stubs[self.i].process_pollution_data.future(pollution_data) # Enviar dato a procesar al compute server seleccionado
        response = sensorLBCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_LBServiceServicer_to_server`
# to add the defined class to the server
sensorLBCom_pb2_grpc.add_LBServiceServicer_to_server(LoadBalancerServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('0.0.0.0:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
