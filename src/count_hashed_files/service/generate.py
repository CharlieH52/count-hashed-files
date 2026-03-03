import os
import subprocess
import json
import re
from collections import defaultdict

class CertifyMaker:
    def __init__(self, target_path: str, output_file_name: str) -> None:
        self.working_path = os.getcwd()
        self.path = target_path
        self.output_name = output_file_name

    def __execute_process(self) -> str:
        try:
            input_command = ['powershell', f'Get-ChildItem -path "{self.path}" -recurse | Get-FileHash -algorithm SHA256 | convertto-json']
            output = subprocess.run(input_command, capture_output=True, text=True, encoding='utf-8', errors='replace')
            return output.stdout
        except:
            return ""

    def __save_json_file(self, data: str, file_name: str) -> None:
        output_file_name = file_name
        json_data = json.loads(data)
        try:
            with open(output_file_name, "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4)
        except PermissionError:
            pass

    def __load_json_file(self, file_path: str) -> list[dict[str,str]]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(e)

    def __get_file_extension_list(self, json_data: list[dict[str,str]]) -> list[dict[str, int]]:
        data_file = json_data
        conteos = defaultdict(int)
        total = 0
        for file in data_file:
            path = file.get("Path")
            if not path:
                continue

            match = re.search(r'\.([a-z0-9]+)$', path.lower())
            if match:
                extension = match.group(1)
                conteos[extension] += 1
                total += 1
        print(f"Archivos totales: {total}")

        return [
            {"extension": ext, "conteo": count}
            for ext, count in conteos.items()
        ]

    def orquestar(self):
        file_name = os.path.join(self.working_path, f"{self.output_name}.json")
        output_json = self.__execute_process()
        self.__save_json_file(output_json, file_name)
        data = self.__load_json_file(file_name)
        count = self.__get_file_extension_list(data)
        for item in count:
            print(f'Extension de archivo: {item.get("extension")} = {item.get("conteo")}')