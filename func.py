# -*- coding: utf-8 -*-

import struct

def Slice(item:bytes, pos:int, len:int):
    return item[pos : pos+len]


def CalcCrc(data:bytes):
    crc = 0
    for i in data:
        val = int(i)
        crc ^= val
    return crc & 0xFF

def EncodeUInt08(val:int):
    return 0 <= val <= 0xFF, struct.pack(">B", val)

def EncodeUInt16(val:int):
    return 0 <= val <= 0xFFFF, struct.pack(">H", val)

def EncodeUInt32(val:int):
    return 0 <= val <= 0xFFFFFFFF, struct.pack(">I", val)

def EncodeUInt64(val:int):
    return 0 <= val <= 0xFFFFFFFFFFFFFFFF, struct.pack(">Q", val)