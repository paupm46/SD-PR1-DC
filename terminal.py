import grpc
import time
from concurrent import futures

import proxyTerminalCom_pb2
import proxyTerminalCom_pb2_grpc

class TerminalServicer(proxyTerminalCom_pb2_grpc.TerminalServiceServicer):

    def send_results(self, coefficients, context):
        print(coefficients) # Aqui s'ha de fer Terminals must represent the data they receive in real time through a simple, visual user interface
        response = proxyTerminalCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_TerminalServiceServicer_to_server`
# to add the defined class to the server
proxyTerminalCom_pb2_grpc.add_TerminalServiceServicer_to_server(TerminalServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50060.')
server.add_insecure_port('0.0.0.0:50060')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)