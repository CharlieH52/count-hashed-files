import os
import subprocess
import json
import re
from collections import defaultdict

working_path = os.getcwd()
path = "E:\\Escritorio\\SISTEMAS"
output_name = "tareas"

def execute_process(target_path: str) -> str:
    try:
        input_command = ['powershell', f'Get-ChildItem -path "{target_path}" -recurse | Get-FileHash -algorithm SHA256 | convertto-json']
        output = subprocess.run(input_command, capture_output=True, text=True, encoding='utf-8', errors='replace')
        return output.stdout
    except:
        return ""

def save_json_file(data: str, file_name: str) -> None:
    output_file_name = file_name
    json_data = json.loads(data)
    try:
        with open(output_file_name, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4)
    except PermissionError:
        pass

def load_json_file(file_path: str) -> list[dict[str,str]]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(e)

def get_file_extension_list(json_data: list[dict[str,str]]) -> list[dict[str, int]]:
    data_file = json_data
    conteos = defaultdict(int)
    for file in data_file:
        path = file.get("Path")
        if not path:
            continue

        match = re.search(r'\.([a-z0-9]+)$', path.lower())
        if match:
            extension = match.group(1)
            conteos[extension] += 1

    return [
        {"extension": ext, "conteo": count}
        for ext, count in conteos.items()
    ]

def orquestar():
    file_name = os.path.join(working_path, f"{output_name}.json")
    output_json = execute_process(path)
    save_json_file(output_json, file_name)
    data = load_json_file(file_name)
    count = get_file_extension_list(data)
    for item in count:
        print(item)

orquestar()