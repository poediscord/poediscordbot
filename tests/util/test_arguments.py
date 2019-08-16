from poediscordbot.util.arguments import Params, Field
from datetime import timedelta
from dataclasses import dataclass
from typing import Optional, List

def test_parser_simple():
    class TestParams(Params):
        group: str
        phrase: str = Field(remaining=True)
    
    assert hasattr(TestParams, "_fields")
    assert len(TestParams._fields) == 2

    tp = TestParams(["group_text", "phrase", "more", "last"])

    assert tp.group == "group_text"
    assert tp.phrase == "phrase more last"

def test_parser_optional():
    class TestParams(Params):
        group: str
        phrase: str = Field(remaining=True)
        warnings: Optional[str]
    
    assert hasattr(TestParams, "_fields")
    assert len(TestParams._fields) == 2
    assert len(TestParams._opt_fields) == 1

    tp = TestParams(["group_text", "-w", "10", "phrase", "more", "last"])

    assert tp.group == "group_text"
    assert tp.phrase == "phrase more last"
    assert tp.warnings == "10"

    tp = TestParams(["group_text", "phrase", "more", "last"])

    assert tp.group == "group_text"
    assert tp.phrase == "phrase more last"
    assert tp.warnings == None

def test_parser_int():
    class TestParams(Params):
        a: int
        b: Optional[int]

    tp = TestParams(["-b", "20", "10"])
    assert tp.a == 10
    assert tp.b == 20

def test_parser_float():
    class TestParams(Params):
        a: float
        b: Optional[float]

    tp = TestParams(["-b", "20", "10"])
    assert tp.a == 10.0
    assert tp.b == 20.0

def test_parser_timedelta():
    class TestParams(Params):
        a: timedelta
        b: Optional[timedelta]
        c: timedelta

    tp = TestParams(["-b", "3w12d1h3m", "2w11d1h2m", "forever"])
    assert tp.a.days == 2*7+11
    assert tp.a.seconds == 1*60*60 + 2*60
    assert tp.b.days == 3*7+12
    assert tp.b.seconds == 1*60*60 + 3*60
    assert tp.c == None