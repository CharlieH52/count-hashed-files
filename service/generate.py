import os
import subprocess
import json
import re
from typing import Any
from collections import defaultdict

class CertifyMaker:
    def __init__(self, target_path: str, output_file_name: str) -> None:
        self.working_path = os.path.join(os.getcwd(), "Certificaciones")
        self.path = target_path
        self.output_name = output_file_name

    # Execute the main process to generate the HASH lines
    def __execute_process(self) -> str:
        try:
            input_command = ['powershell', f'Get-ChildItem -path "{self.path}" -recurse | Get-FileHash -algorithm SHA256 | convertto-json']
            output = subprocess.run(input_command, capture_output=True, text=True, encoding='utf-8', errors='replace')
            return output.stdout
        except subprocess.CalledProcessError.stderr as e:
            return e

    # Create a JSON file
    def __save_process(self, incoming_data: list[dict[str,Any]], path: str):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(incoming_data, file, indent=4)

    # Load a string with JSON format and use save_process to create the file
    def __save_json_file(self, data: str, file_name: str) -> None:
        try:
            output_data = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON invalido: {e}")
        # Checks if the incoming string has a valid JSON format
        if not isinstance(output_data,list):
            output_data = [output_data]

        try:
            self.__save_process(output_data,file_name)
        except PermissionError as e:
            raise PermissionError(f"No se pudo escribir el archivo: {file_name}") from e

    # Load a JSON file
    def __load_json_file(self, file_path: str) -> list[dict[str,Any]]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                output = json.load(file)
                # Checks if the incoming JSON is List[Dict] or Dict,
                # always return a List[Dict]
                if isinstance(output, list):
                    return output
                else:
                    return [output]
        except json.JSONDecodeError as e:
            print(e)
            return []
    
    # Returns the file extension with the counted files per file extension
    def __get_file_extension_list(self, json_data: list[dict[str,Any]]) -> list[dict[str,int]]:
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

    def process(self) -> list[dict[str,Any]]:
        file_name = os.path.join(self.working_path, f"{self.output_name}.json")
        output_json = self.__execute_process()
        self.__save_json_file(output_json, file_name)
        data = self.__load_json_file(file_name)
        count = self.__get_file_extension_list(data)
        return count