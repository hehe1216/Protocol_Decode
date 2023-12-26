# -*- coding: utf-8 -*-

from msg_txj import *
from msg_8103 import *
from readjson import *


if __name__ == "__main__":
    # 获取当前脚本所在的目录
    path = os.path.dirname(os.path.abspath(__file__))
    # 输出目录路径
    print("dir: " + path)
    argv = "7E8103000A332309233542C3BB010000F24D0400010007017E"
    #code = bytes.fromhex(sys.argv[1])
    code = bytes.fromhex(argv)

    print("---------------------808消息解析----------------------")
    txjmsg = TMsgTxj()
    txjmsg.Decode(code)
    txjmsg.printcode()

    print("-----------------------消息体解析----------------------")
    if txjmsg.GetCmdUnit() == 0x8103:
        msg8103 = TMsg8103()   
        msg8103.Decode(txjmsg.GetDataUnit())
        msg8103.printParamList()

        print("--------------------8103参数值解析-----------------------")
        param_data_list = msg8103.GetParamList()
        for paraminfo in param_data_list:
            paramid = int(paraminfo[0].hex(), 16)
            paramlen = int(paraminfo[1].hex(), 16)
            paramdata = paraminfo[2].hex()
            print(f"{paramid}--{type(paramid)}, {paramlen}--{type(paramlen)}, {paramdata}--{type(paramdata)}")
            if paramid == 0x0000F364:
                print("8103-0x0000F364")
                print(f"{paramlen} -- {paramdata}")
                pass
            if paramid == 0x0000F365:
                print("8103-0x0000F365")
                print(f"{paramlen} -- {paramdata}")
                pass
            if paramid == 0x0000F257:
                print("8103-0x0000F257")
                print(f"{paramlen} -- {paramdata}")
                pass
            if paramid == 0x0000F258:
                print("8103-0x0000F258")
                print(f"{paramlen} -- {paramdata}")
                pass
            if paramid == 0x0000F24D:
                print("8103-0x0000F24D")
                print(f"{paramlen} -- {paramdata}-{type(paramdata)}")
                msgF240 = Msg8103F24D()   
                msgF240.decode(bytes.fromhex(paramdata))
                print(msgF240.render_template())
                pass
