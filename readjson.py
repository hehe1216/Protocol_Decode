import json

def read_json_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"读取 JSON 文件错误: {e}")
        return None
    
def extract_command_info(parsed_data):
    command_info = {}

    unit_cmd_data = parsed_data.get("unit_cmd", {})
    if isinstance(unit_cmd_data, dict):
        for cmd_id, cmd_list in unit_cmd_data.items():
            command_info[cmd_id] = []
            for cmd_item in cmd_list:
                for cmd_name, params in cmd_item.items():
                    cmd_info = {"paramId": cmd_name, "parameters": []}
                    for param in params:
                        if isinstance(param, dict):
                            for param_name, param_value in param.items():
                                if isinstance(param_value, list):
                                    param_info = {"name": param_name, "fields": param_value}
                                    print(param_info)
                                    cmd_info["parameters"].append(param_info)

                    command_info[cmd_id].append(cmd_info)

    return command_info

if __name__ == "__main__":
    json_filename = "protocol.json"
    json_data = read_json_from_file(json_filename)

    if json_data:
        command_info = extract_command_info(json_data)
        print(command_info)
