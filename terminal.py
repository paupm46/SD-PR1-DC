import grpc
import time
from concurrent import futures
import matplotlib.pyplot as plt
import sys
import pytz

import proxyTerminalCom_pb2
import proxyTerminalCom_pb2_grpc

wellness_means = []
pollution_means = []
timestamps = []


class TerminalServicer(proxyTerminalCom_pb2_grpc.TerminalServiceServicer):
    def send_results(self, coefficients, context): # Procedimiento llamado por el proxy
        # Añadir a las respectivas listas los coeficientes (y timestamp) recibidos
        global wellness_means, pollution_means, timestamps
        wellness_means.append(coefficients.wellness_mean)
        pollution_means.append(coefficients.pollution_mean)
        cet_tz = pytz.timezone('CET')
        utc_tz = pytz.timezone('UTC')
        utc_now = coefficients.timestamp.ToDatetime()
        timestamps.append(utc_tz.localize(utc_now).astimezone(cet_tz).strftime('%H:%M:%S.%f'))
        animate() # Actualizar gráfica
        response = proxyTerminalCom_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_TerminalServiceServicer_to_server`
# to add the defined class to the server
proxyTerminalCom_pb2_grpc.add_TerminalServiceServicer_to_server(TerminalServicer(), server)

port = 50060 + int(sys.argv[1])

# listen on port
print('Starting server. Listening on port ' + str(port) + '.')
server.add_insecure_port('0.0.0.0:' + str(port))
server.start()

fig = plt.figure(figsize=(12, 6))
ax = plt.subplot(121)
ax2 = plt.subplot(122)


def animate(): # Procedimiento para actualizar gráfica
    global wellness_means, pollution_means, timestamps
    timestamps = timestamps[-20:]
    wellness_means = wellness_means[-20:]
    pollution_means = pollution_means[-20:]

    ax.clear()
    ax.plot(timestamps, wellness_means)
    ax.tick_params(labelrotation=45)

    ax2.clear()
    ax2.plot(timestamps, pollution_means)
    ax2.tick_params(labelrotation=45)

    ax.title.set_text('Air wellness')
    ax2.title.set_text('Air pollution')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Coefficient')
    ax2.set_xlabel('Timestamp')
    ax2.set_ylabel('Coefficient')

    plt.subplots_adjust(bottom=0.30)
    plt.draw()


plt.show()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
