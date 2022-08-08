# _pb2.py 和 _pb2_grpc.py文件通过以下命令生成

python -m grpc_tools.protoc -I=./proto --python_out=./grpc_module --grpc_python_out=./grpc_module sensitive.proto