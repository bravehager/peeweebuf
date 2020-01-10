# peeweebuf

Write database-driven gRPC services with minimal boilerplate using [peewee](https://github.com/coleifer/peewee).

The primary goal of this package is to grant strong guarantees that peewee models will reflect gRPC defined message schemas, without the hassle of managing both.

**This pacakge is proof of concept, for the most part.** 

## Examples

gRPC serivce definition:
```proto3
service UserService {
  rpc GetById(UserRequest) returns (User);
  rpc Insert(User) returns (User);
}

message User {
  int32 id = 1;
  string username = 2;
  string email = 3;
}

message UserRequest { int32 id = 1; }
```

Corresponding peewee-backed service:

```python3
from peewee import *
from peeweebuf import Proto, peewee_to_proto, proto_to_dict

from user_pb2 import TransactionStatus, User as UserProto
from user_pb2_grpc import UserServiceServicer as UserService, \
    add_UserServiceServicer_to_server as add_user_servicer

@Proto(UserProto, primary_key='id')
class User(Model, UserService):
    class Meta:
        database = db

    @peewee_to_proto(UserProto)
    def GetById(self, request, context):
        return User[request.id]

    @peewee_to_proto(UserProto)
    def Insert(self, request, context):
        return User.create(**proto_to_dict(request))

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
add_user_servicer(User(), server)

server.add_insecure_port('[::]:50051')
server.start()
```


