import typing
import argparse
import re
from collections import OrderedDict, namedtuple
from enum import Enum
from datetime import timedelta, datetime
from poediscordbot.core.model import UserId

_FieldData = namedtuple("field_data", ['name', 'type', 'value'])

class ParamsMeta(type):
    def __init__(cls, name, bases, ns):
        fields = []
        opt_fields = {}
        remaining = False
        
        if "__annotations__" in cls.__dict__:
            for f_name, f_type in cls.__dict__["__annotations__"].items():
                                
                if hasattr(cls, f_name):
                    f_value = getattr(cls, f_name)
                else:
                    f_value = None

                if hasattr(f_type, "__origin__") and f_type.__origin__._name == "Union" \
                    and type(None) in f_type.__args__:
                    # its optional
                    opt_fields[f_name[0]] = _FieldData(f_name, f_type, f_value)
                else:
                    if isinstance(f_value, Field):
                        if f_value.remaining:
                            remaining = f_name
                    fields.append( _FieldData(f_name, f_type, f_value) )

        if not hasattr(cls, "_fields"):
            cls._fields = fields
        else:
            cls._fields = cls._fields + fields

        if not hasattr(cls, "_opt_fields"):
            cls._opt_fields = opt_fields
        else:
            cls._opt_fields = dict(**cls._opt_fields, **opt_fields)
        cls._remaining = remaining

class Params(metaclass=ParamsMeta):
    def __init__(self, args):
        fields_to_do: typing.List[_FieldData] = list(self.__class__._fields)
        opt_to_do: typing.Dict[str, _FieldData] = dict(self.__class__._opt_fields)
        remaining = None
        in_opt: typing.Optional[_FieldData] = None

        for w in args:
            if len(w) == 2 and w[0] == "-":
                if w[1] in opt_to_do:
                    # found optional param
                    in_opt = opt_to_do[w[1]]
                    del opt_to_do[w[1]]
                else:
                    raise Exception(f"Invalid optional param: {w[1]}")
            elif in_opt:
                setattr(self, in_opt.name, convert(w, in_opt))
                in_opt = None
            elif remaining or (len(fields_to_do)==1 and isinstance(fields_to_do[0].value, Field) and \
                fields_to_do[0].value.remaining):
                # we are in or starting the 'remaining' parameter
                remaining = remaining or []
                remaining.append(w)
            elif len(fields_to_do)>0:
                field = fields_to_do.pop(0)
                setattr(self, field.name, convert(w, field))
            else:
                raise Exception("Too many parameters!")
        if remaining:
            setattr(self, fields_to_do[0].name, " ".join(remaining))
        if opt_to_do:
            for f_name, field_data in opt_to_do.items():
                setattr(self, field_data.name, None)


class Field:
    def __init__(self, remaining=False):
        self.remaining = remaining

    def __repr__(self):
        return f"<Field: remaining={self.remaining}>"

_converters = {}

def convert(value, field_data):
    f_name, f_type, f_value = field_data
    if hasattr(f_type, "__origin__") and f_type.__origin__._name == "Union" \
                and type(None) in f_type.__args__:
        options = f_type.__args__
    else:
        options = [f_type]
    for opt in options:
        if opt is str:
            return value
        elif opt in _converters:
            return _converters[opt](value)
    raise Exception("Could not convert value")

class converter:
    """Decorator to mark a function as being used to convert from a string
    to a specific type
    
    The function should throw an exception if it is unable to do the conversion."""

    def __init__(self, cls):
        self.cls = cls

    def __call__(self, func):
        _converters[self.cls] = func
        return func

td_regex_parser = re.compile(r"(?:(\d+)([ywdhm]))")

@converter(timedelta)
def convert_to_timedelta(data):
    if data == "forever":
        return None
    days = 0
    seconds = 0

    for segment in td_regex_parser.finditer(data):
        num, seg = segment.groups()
        if seg == "w":
            days += 7*int(num)
        elif seg == "y":
            days += 365*int(num)
        elif seg == "d":
            days += int(num)
        elif seg == "h":
            seconds += 60*60*int(num)
        elif seg == "m":
            seconds += 60*int(num)
        else:
            raise Exception("Invalid duration")
    
    return timedelta(days=days, seconds=seconds)

@converter(datetime)
def convert_to_datetime(data):
    td = convert_to_timedelta(data)
    
    return datetime.utcnow() + td

@converter(int)
def convert_to_int(data):
    return int(data)

@converter(float)
def convert_to_float(data):
    return float(data)
