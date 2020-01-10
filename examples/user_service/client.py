import grpc

from user_pb2 import UserRequest, User
from user_pb2_grpc import UserServiceStub

channel = grpc.insecure_channel('localhost:50051')
user_stub = UserServiceStub(channel)

user = User(id=1, username='JohnDoe', email='john@gmail.com')
response = user_stub.Insert(user)
print(response)

response = user_stub.GetById(UserRequest(id=1))
print(response)