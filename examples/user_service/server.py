import time
import grpc
from concurrent import futures

from peewee import *
from playhouse.cockroachdb import CockroachDatabase
from peeweebuf import Proto, peewee_to_proto, proto_to_dict

from user_pb2 import User as UserProto
from user_pb2_grpc import UserServiceServicer as UserService, \
    add_UserServiceServicer_to_server as add_user_servicer

db = CockroachDatabase('dev', user='root', port=26257, host='127.0.0.1')


@Proto(UserProto, primary_key='id')
class User(Model, UserService):
    class Meta:
        database = db

    @peewee_to_proto(UserProto)
    def GetById(self, request, context):
        return User[request.id]

    @peewee_to_proto(UserProto)
    def GetAll(self, request, context):
        return User.select()

    @peewee_to_proto(UserProto)
    def Insert(self, request, context):
        try:
            return User.create(**proto_to_dict(request))
        except IntegrityError as e:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('user already exists')


db.drop_tables([User])
db.create_tables([User])

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
add_user_servicer(User(), server)

server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)