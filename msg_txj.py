# -*- coding: utf-8 -*-

import os
import sys
import struct
from func import *



class TMsgTxj:
    def __init__(self) -> None:
        self.begin_flag = b'\x7E'
        self.cmd_unit = b''
        self.msg_attr = b''
        self.ter_id = b''
        self.msg_serial = b''
        self.data_unit = b''
        self.crc = b''
        self.end_flag = b'\x7E'

    def SetBeginFlag(self, beginFlag:int):
        valid, self.begin_flag = EncodeUInt08(beginFlag)
        return valid

    def GetBeginFlag(self):
        return self.begin_flag

    def SetCmdUnit(self, cmd:int):
        valid, self.cmd_uint = EncodeUInt16(cmd)
        return valid
    
    def GetCmdUnit(self):
        val = 0xFFFF
        if len(self.cmd_unit) == 2:
            val = struct.unpack(">H", self.cmd_unit)[0]
        return val
    
    def SetMsgAttr(self, val:int):
        valid, self.msg_attr = EncodeUInt16(val)
        return valid
    
    def GetMsgAttr(self):
        val = 0xFFFF
        if len(self.msg_attr) == 2:
            val = struct.unpack(">H", self.msg_attr)[0]
        return val
    
    def SetTerId(self, val:str):
        valid = True
        if len(val) != 6:
            valid = False
        else:
            self.ter_id = struct.pack(">6s", val)
        return valid
    
    def GetTerId(self):
        val = ""
        if len(self.ter_id) == 6:
            val = struct.unpack(">6s", self.ter_id)[0]
        return val
    
    def SetMsgSerial(self, val:int):
        valid, self.msg_serial = EncodeUInt16(val)
        return valid
    
    def GetMsgSerial(self):
        val = 0xFFFF
        if len(self.msg_serial) == 2:
            val = struct.unpack(">H", self.msg_serial)[0]
        return val
    
    def SetDataUnit(self, val:bytes):
        valid = False
        if len(val) == self.GetMsgAttr():
            self.data_unit = val
            valid = True
        return valid

    def GetDataUnit(self):
        return self.data_unit

    def SetCrc(self, val:int):
        valid, self.crc = EncodeUInt08(val)
        return valid

    def GetCrc(self):
        val = 0xFF
        if len(self.crc) == 1:
            val = struct.unpack(">B", self.crc)[0]
        return val

    def SetEndFlag(self, endFlag:int):
        valid, self.end_flag = EncodeUInt08(endFlag)
        return valid

    def GetEndFlag(self):
        return self.end_flag

    def Decode(self, code:bytes):
        limt = 1 + 2 + 2 + 6 + 2 + 1 + 1
        if code.__len__() < limt:
            return False
        pos = 0

        # 起始符
        len = 1
        item = Slice(code, pos, len)
        if item != b'\x7E':
            return False
        self.begin_flag = item
        pos += len

        # 消息ID
        len = 2
        item = Slice(code, pos, len)
        self.cmd_unit = item
        pos += len

        # 消息体属性
        len = 2
        item = Slice(code, pos, len)
        self.msg_attr = item
        pos += len

        # 终端手机号
        len = 6
        item = Slice(code, pos, len)
        self.ter_id = item
        pos += len

        # 消息流水号
        len = 2
        item = Slice(code, pos, len)
        self.msg_serial = item
        pos += len

        # 消息体
        len = code.__len__() - pos - 2
        data_unit_len = self.GetMsgAttr()
        if (len != data_unit_len):
            return False
        item = Slice(code, pos, len)
        self.data_unit = item
        pos += len

        # 校验码
        crc = CalcCrc(code[1 : -2])
        if(crc != int(code[-2])):
            return False
        self.crc = crc
        

        # 终止符
        item = code[-1]
        if item != b'\x7E':
            return False
        self.end_flag = item
        return True
    
    def printcode(self):
        begin_hex = self.begin_flag.hex()
        cmd_unit_hex = self.cmd_unit.hex()
        msg_attr_hex = self.msg_attr.hex()
        ter_id_hex = self.ter_id.hex()
        msg_serial_hex = self.msg_serial.hex()
        data_unit_hex = self.data_unit.hex()
        crc_hex = hex(self.crc)
        end_hex = self.end_flag.hex()
        
        print(f"起始字符：  {begin_hex}")
        print(f"消息ID:     {cmd_unit_hex}")
        print(f"消息体属性：{msg_attr_hex}")
        print(f"终端号：    {ter_id_hex}")
        print(f"消息流水号：{msg_serial_hex}")
        print(f"消息体：    {data_unit_hex}")
        print(f"校验码：    {crc_hex}")
        print(f"终止字符：  {end_hex}")
        
        return True
    
if __name__ == "__main__":
    # 获取当前脚本所在的目录
    path = os.path.dirname(os.path.abspath(__file__))
    # 输出目录路径
    print("dir: " + path)
    code = bytes.fromhex(sys.argv[1])
    
    txjmsg = TMsgTxj()
    txjmsg.Decode(code)
    txjmsg.printcode()
    
    
    


