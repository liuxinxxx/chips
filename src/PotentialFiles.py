from typing import Any

class PotentialFiles():
    '文件类--包含文件类型和该类文件的路径数组'
    'File Object--Includes two attribute, the type of format file_type; the path list of these files'

    def __init__(self,file_type,path) -> None:
        self.file_type=file_type
        self.path=path

    def __sizeof__(self) -> int:
        return len(self.path)
    