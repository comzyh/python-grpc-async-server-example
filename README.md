# python-grpc-async-server-example

# Generate proto

To generate server and client code from `example.proto`, make sure you have grpc_tools

> pip3 install grpcio_tools

Generate code

> python3 -m grpc_tools.protoc -I.  --python_out=. --grpc_python_out=. protocol/example.proto
