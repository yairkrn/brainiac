import datetime as dt
import struct

import pytest

from brainiac import protocol


_USER_ID = 1337
_USERNAME = 'Yair Karin'
_BIRTHDAY = dt.datetime(2020, 12, 20)
_GENDER = 'm'


def test_hello_build():
    message = protocol.HelloMessage.build(dict(user_id=_USER_ID,
                                               username=_USERNAME,
                                               birthday=_BIRTHDAY,
                                               gender=_GENDER))
    expected = struct.pack('<QI', _USER_ID, len(_USERNAME)) + \
        _USERNAME.encode() + struct.pack('<I', int(_BIRTHDAY.timestamp())) + \
        _GENDER.encode()
    assert message == expected


def test_hello_parse():
    encoded_message = struct.pack('<QI', _USER_ID, len(_USERNAME)) + \
        _USERNAME.encode() + struct.pack('<I', int(_BIRTHDAY.timestamp())) + \
        _GENDER.encode()
    parsed = protocol.HelloMessage.parse(encoded_message)
    assert parsed.user_id == _USER_ID
    assert parsed.username == _USERNAME
    assert parsed.birthday == _BIRTHDAY
    assert parsed.gender == _GENDER


_SUPPORTED_FIELDS_NUM = 3
_SUPPORTED_FIELDS = ["Field1", "f1", "f2"]


def test_config_build():
    message = protocol.ConfigMessage.build(dict(
        supported_fields_number=_SUPPORTED_FIELDS_NUM,
        supported_fields=_SUPPORTED_FIELDS))
    expected = struct.pack('<I', _SUPPORTED_FIELDS_NUM) + \
        b''.join(
            [struct.pack('<I', len(f)) + f.encode() for f in _SUPPORTED_FIELDS]
        )
    assert message == expected


def test_config_parse():
    encoded_message = struct.pack('<I', _SUPPORTED_FIELDS_NUM) + \
        b''.join(
            [struct.pack('<I', len(f)) + f.encode() for f in _SUPPORTED_FIELDS]
        )
    parsed = protocol.ConfigMessage.parse(encoded_message)
    assert parsed.supported_fields_number == _SUPPORTED_FIELDS_NUM
    assert parsed.supported_fields == _SUPPORTED_FIELDS
