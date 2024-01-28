from io import TextIOWrapper
from typing import Optional

from ur_objects_savers.base_ur_saver import BaseSaver


class FileSaver(BaseSaver):
    _filename: str
    _filestream: Optional[TextIOWrapper]

    def __init__(self, path_to_file: str):
        super().__init__()
        self._filename = path_to_file
        self._filestream = None

    def __enter__(self):
        self._filestream = open(self._filename, "w")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._filestream.close()

    def save(self, obj_repr: str):
        self._filestream.write(obj_repr)
        self._filestream.write('\n')
