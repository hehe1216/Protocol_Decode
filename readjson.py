import json

class JsonParameter:
    def __init__(self, name: str, length: str):
        self.name = name
        self.length = length

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(json_data.get("name", ""), json_data.get("length", ""))

class JsonCommand:
    def __init__(self, cmd_data: list):
        self.command_data = cmd_data

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(json_data)

    def get_parameters(self):
        parameters = []
        for param_id, param_data in self.command_data.items():
            for pdata in param_data:
                parameter = JsonParameter.from_json({"name": pdata, "length": pdata})
                parameters.append(parameter)
        return  param_id, parameters

class JsonCommandInfo:
    def __init__(self, unit_cmd: dict):
        self.unit_cmd = unit_cmd

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(json_data.get("unit_cmd", {}))

    def get_commands(self):
        commands = []
        for cmd_id, cmd_list in self.unit_cmd.items():
            for cmd_data in cmd_list:
                command = JsonCommand.from_json(cmd_data)
                commands.append(command)
        return commands

class ReadJsonFromFile:
    def __init__(self, filename: str):
        self.filepath = filename

    def get_data_from_file(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"读取 Json 文件错误：{e}")
            return None


class ReadJsonParam:
    def __init__(self, filename:str, paramId:int):
        self.filename = filename
        self.paramId = paramId
    
    def get_paramlist(self):
        r = ReadJsonFromFile(self.filename)
        json_data = r.get_data_from_file()

        commands_info = JsonCommandInfo.from_json(json_data)
        commands = commands_info.get_commands()

        for command in commands:
            paramid, parameters = command.get_parameters()
            if paramid == self.paramId:
                paramlists = []
                for param in parameters:
                    print(f"{param}")
                    paramlist = []
                    name = param.name.get("name", "")
                    length = param.length.get("length", "")
                    paramlist.append(name)
                    paramlist.append(length)
                paramlists.append(paramlist)
        return paramlists


if __name__ == "__main__":
    json_filename = "protocol.json"
    r = ReadJsonFromFile(json_filename)
    json_data = r.get_data_from_file()
    print(f"{json_data}")

    commands_info = JsonCommandInfo.from_json(json_data)
    commands = commands_info.get_commands()
   
    for command in commands:
        paramid, parameters = command.get_parameters()
        print(f"{paramid}")
        for param in parameters:
            print(f"{param.name} {param.length}")
            name = param.name.get("name", "")
            print(f"{name}")
            length = param.length.get("length", "")
            print(f"{length}")

