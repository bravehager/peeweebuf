import grpc

from user_pb2 import UserRequest, User, Empty
from user_pb2_grpc import UserServiceStub

channel = grpc.insecure_channel('localhost:50051')
user_stub = UserServiceStub(channel)


def insert_user(user):
    response = user_stub.Insert(user)
    return response


def get_all_users():
    response = user_stub.GetAll(Empty())
    return response


def get_user_by_id(user_request):
    response = user_stub.GetById(user_request)
    return response


response = insert_user(User(id=1, username='johndoe', email='john@gmail.com'))
print(response)

user = get_user_by_id(UserRequest(id=1))
print(user)

users = get_all_users()
for user in users:
    print(user)