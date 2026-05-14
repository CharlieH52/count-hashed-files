import os
import subprocess
import json
import re
import wmi
from typing import Any
from collections import defaultdict

class CertifyMaker:
    def __init__(self, target_path: str, output_file_name: str) -> None:
        self.working_path = os.path.join(os.getcwd(), "Certificaciones")
        self.__check_output_directory()
        self.saved_file_path = os.path.join(self.working_path, f"{output_file_name}.json")
        self.path = target_path
        self.mount_point = self.__get_parced_logic_drive(self.path)
        self.drive_size = self.__get_logical_drive_inf(self.mount_point)

        self.output_json = self.__execute_process()
        self.__save_json_file(self.output_json, self.saved_file_path)

        self.current_data = self.__load_json_file(self.saved_file_path)

    # Execute the main process to generate the HASH lines
    def __execute_process(self) -> str:
        try:
            input_command = [
                "powershell",
                "-NoProfile",
                "-Command",
                f"""
                [Console]::OutputEncoding = [System.Text.Encoding]::UTF8;
                $OutputEncoding = [System.Text.Encoding]::UTF8;
                Get-ChildItem -Path '{self.path}' -Recurse |
                Get-FileHash -Algorithm SHA256 |
                ConvertTo-Json -Depth 3
                """
            ]
            output = subprocess.run(input_command, capture_output=True)
            raw = output.stdout
            text = raw.decode("utf-8")
            return text
        except subprocess.SubprocessError as e:
            print(e)

    # Bites converter
    def __get_size(self, size: int):
        units = ["B", "KB", "MB", "GB", "TB"]
        value = float(size)

        for unit in units:
            if value < 1024:
                return round(value, 2), unit
            value /= 1024

        return round(value, 2), "PB"

    # Parse the path to obtain the mount point
    def __get_parced_logic_drive(self, path: str) -> str:
        return path.split("\\")[0]

    # Get full data from the mount device
    def __get_logical_drive_inf(self, mount: str):
        c = wmi.WMI()
        for disk in c.Win32_LogicalDisk():
            if disk.DeviceID == mount:
                return disk

    # Get max size from device
    def get_logical_drive_size(self):
        used_size = self.__get_size(int(self.drive_size.Size))
        return f"{used_size[0]} {used_size[1]}"

    # Get free space from device
    def get_logical_drive_free_space(self):
        free_size = self.__get_size(int(self.drive_size.FreeSpace))
        return f"{free_size[0]} {free_size[1]}"

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
    def get_file_extension_list(self) -> list[dict[str,int]]:
        conteos = defaultdict(int)
        for file in self.current_data:
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
    
    def get_used_space(self) -> str:
        sum = 0
        errrs = []
        for file in self.current_data:
            path = file.get("Path")
            try:
                file_obj = os.stat(path)
                sum = sum + int(os.stat_result(file_obj).st_size)
            except Exception as e:
                errrs.append((path, str(e)))
                print(errrs)
        bar = self.__get_size(sum)
        return f"{bar[0]} {bar[1]}"
    
    def __check_output_directory(self):
        if not os.path.exists(self.working_path):
            try:
                os.mkdir(self.working_path)
            except PermissionError as e:
                print(e)