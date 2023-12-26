# -*- coding: utf-8 -*-

import struct
import os
import sys
from func import *
from typing import List
from readjson import *

class TMsg8103():
    def __init__(self) -> None:
        self.code = b''
        self.code_len = 0
        self.paramCnt = 0
        self.paramId = b''
        self.param_len = 0
        self.param_val = b''
        self.param_list = []

    def SetCodeInfo(self, code:str, length:int):
        valid = True
        if len(code) != length:
            valid = False
        else:
            self.code = struct.pack(">{length}s", code)
            self.code_len = length
        return valid
    
    def GetCodeInfo(self):
        val = ""
        if len(self.code) == self.code_len:
            val = struct.unpack(">{self.code_len}s", self.code)[0]
        return val, self.code_len

    def SetParamCnt(self, count:int):
        valid, self.paramCnt = EncodeUInt08(count)
        return valid
    
    def GetParamCnt(self):
        val = 0xFF
        if len(self.paramCnt) == 1:
            val = struct.unpack(">B", self.paramCnt)[0]
        return val
    
    def SetParamId(self, id:int):
        valid, self.paramId = EncodeUInt32(id)
        return valid
    
    def GetParamId(self):
        val = 0xFFFFFFFF
        if len(self.paramId) == 4:
            val = struct.unpack(">I", self.paramId)[0]
        return val
    
    def SetParamLen(self, length:int):
        valid, self.param_len = EncodeUInt08(length)
        return valid
    
    def GetParamLen(self):
        val = 0xFF
        if len(self.param_len) == 1:
            val = struct.unpack(">B", self.param_len)[0]
        return val
    
    def SetParamVal(self, val:bytes):
        valid = False
        if len(val) == self.GetParamLen():
            self.param_val = val
            valid = True
        return valid
    
    def GetParamList(self):
        return self.param_list
    

    def Decode(self, code:bytes):
        limit = 1 + 4 + 1
        if code.__len__() < limit:
            return False
        pos = 0

        # 参数总数
        len = 1
        item = Slice(code, pos, len)
        self.paramCnt = item
        pos += len
        
        for i in range(ord(self.paramCnt)):
            paramlist = []
            # 参数ID
            len = 4
            item = Slice(code, pos, len)
            self.paramId = item
            pos += len

            # 参数长度
            len = 1
            item = Slice(code, pos, len)
            self.param_len = item
            pos += len

            # 参数值
            len = ord(self.param_len)
            item = Slice(code, pos, len)
            self.param_val = item
            pos += len

            paramlist.append(self.paramId)
            paramlist.append(self.param_len)
            paramlist.append(self.param_val)

            self.param_list.append(paramlist)

        return True


    def printParamList(self):
        # 参数总数 
        length = len(self.param_list)
        print(f"参数总数： {length}")   
        
        for l in range(length):
            paramlist = self.param_list[l]
            paramId = paramlist[0].hex()
            param_len = paramlist[1].hex()
            param_val = paramlist[2].hex()

            print(f"参数ID:    {paramId}")
            print(f"参数长度： {param_len}")
            print(f"参数值：   {param_val}")

        return True

class MessageBase:
    def __init__(self, code_len: int, parameters):
        self.code_len = code_len
        self.parameters = parameters

    def decode(self, code: bytes):
        if len(code) != self.code_len:
            print("参数长度错误，请检查")
            return False

        pos = 0
        for param in self.parameters:
            item_length = param.length
            item_value = Slice(code, pos, item_length)
            pos += item_length
            param.set_value(item_value)

        return True

    def render_template(self) -> str:
        template_str = ""
        for param in self.parameters:
            template_str += f"{param.name}: {param.value.hex()}\n"
        return template_str



class msg_8103_Parameter:
    def __init__(self, name: str, length: int):
        self.name = name
        self.length = length
        self.value: bytes = b''

    def set_value(self, value: bytes):
        self.value = value

class Msg8103_ID(MessageBase):
    def __init__(self, paramId:int, parameterslist:dict):
        self.paramId = paramId
        self.parametersList = parameterslist
        super().__init__(code_len=4, parameters=self.parametersList)
        # parameters_list = [
        #     msg_8103_Parameter(name="通道视频开关", length=2),
        #     msg_8103_Parameter(name="通道视频开关使能", length=2),
        # ]
        # super().__init__(code_len=4, parameters=parameters_list)


if __name__ == "__main__":
    # 获取当前脚本所在的目录
    path = os.path.dirname(os.path.abspath(__file__))
    # 输出目录路径
    print("dir: " + path)
    code = bytes.fromhex(sys.argv[1])

    msg = TMsg8103()   
    msg.Decode(code)
    msg.printParamList()

    msgF240code = msg.param_list[0][2]
    msgF240 = Msg8103F24D()   
    msgF240.decode(msgF240code)
    print(msgF240.render_template())

