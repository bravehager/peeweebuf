from collections.abc import Generator, Iterable

from google.protobuf.descriptor import FieldDescriptor as fields
from google.protobuf.json_format import MessageToDict as proto_to_dict

from peewee import DoubleField, FloatField, BigIntegerField, IntegerField, \
    FixedCharField, ForeignKeyField, BlobField, BooleanField, CharField

__version__ = '0.0.1'

PROTOBUF_FIELD_IDENTIFIER = "<class 'google.protobuf.pyext._message.FieldProperty'>"


class PeeweeBufError(Exception):
    pass


class TypeConversionError(PeeweeBufError):
    pass


class SerializationError(PeeweeBufError):
    pass


class Proto:
    type_conversion_map = {
        fields.TYPE_DOUBLE: DoubleField,
        fields.TYPE_FLOAT: FloatField,
        fields.TYPE_BOOL: BooleanField,
        fields.TYPE_BYTES: BlobField,
        fields.TYPE_INT32: IntegerField,
        fields.TYPE_INT64: BigIntegerField,
        fields.TYPE_STRING: CharField
    }

    def __init__(self, proto, primary_key=None):
        self._proto = proto
        self._pk = primary_key

    def is_proto_field(obj):
        return str(type(obj)) == PROTOBUF_FIELD_IDENTIFIER

    def __call__(self, cls):
        cls._proto = self._proto
        type_conversion_map = Proto.type_conversion_map

        for name, value in self._proto.__dict__.items():
            if not Proto.is_proto_field(value):
                continue

            if hasattr(cls, name):
                continue

            is_pk = self._pk == name
            field = type_conversion_map.get(value.DESCRIPTOR.type)
            if field is None:
                raise TypeConversionError(
                    "Could not find type conversion for `{}`, try declaring using peewee explicitly."
                    .format(name))

            field = field(primary_key=is_pk)
            if is_pk:
                cls._meta.set_primary_key(name, field)
            cls._meta.add_field(name, field)

        return cls


def peewee_to_proto(Proto):
    def to_proto(peewee_obj):
        try:
            return Proto(**peewee_obj.__dict__['__data__'])
        except Exception as e:
            raise SerializationError(
                'could not convert peewee object to protocol buffer')

    def wrapper(function):
        def inner(*args):
            obj = function(*args)
            if obj is None:
                return obj

            if isinstance(obj, (Iterable, Generator)):
                return iter([to_proto(elem) for elem in obj])
            return to_proto(obj)

        return inner

    return wrapper
