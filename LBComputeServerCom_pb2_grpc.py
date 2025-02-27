# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import LBComputeServerCom_pb2 as LBComputeServerCom__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class ComputeServerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.process_meteo_data = channel.unary_unary(
                '/ComputeServerService/process_meteo_data',
                request_serializer=LBComputeServerCom__pb2.RawMeteoData2.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.process_pollution_data = channel.unary_unary(
                '/ComputeServerService/process_pollution_data',
                request_serializer=LBComputeServerCom__pb2.RawPollutionData2.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class ComputeServerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def process_meteo_data(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def process_pollution_data(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ComputeServerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'process_meteo_data': grpc.unary_unary_rpc_method_handler(
                    servicer.process_meteo_data,
                    request_deserializer=LBComputeServerCom__pb2.RawMeteoData2.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'process_pollution_data': grpc.unary_unary_rpc_method_handler(
                    servicer.process_pollution_data,
                    request_deserializer=LBComputeServerCom__pb2.RawPollutionData2.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ComputeServerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ComputeServerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def process_meteo_data(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ComputeServerService/process_meteo_data',
            LBComputeServerCom__pb2.RawMeteoData2.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def process_pollution_data(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ComputeServerService/process_pollution_data',
            LBComputeServerCom__pb2.RawPollutionData2.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
