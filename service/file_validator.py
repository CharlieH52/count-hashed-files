import os

class Validator:
    def __init__(self, path: str, file_name: str) -> None:
        self.path = path
        self.file_name = file_name
        self.full_path = os.path.join(path, file_name)
    
    def valid_file_name(self) -> bool:
        if os.path.exists(self.full_path):
            return False
        return True
    
    def valid_mount_point(self) -> bool:
        return os.path.ismount(self.path)
    
    def valid_dir_path(self) -> bool:
        return os.path.isdir(self.path)