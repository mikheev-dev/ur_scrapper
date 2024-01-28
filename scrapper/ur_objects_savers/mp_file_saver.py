from multiprocessing import Process, Queue

from scrapper.finish_object import FINISH_OBJECT
from scrapper.ur_objects_savers.file_saver import FileSaver
from scrapper.ur_objects_serializers.base_object_serializer import BaseSerializer


class MPFileSaver(Process):
    _q: Queue
    _fs: FileSaver
    _serializer: BaseSerializer

    def __init__(self, q: Queue, file_saver: FileSaver, serializer: BaseSerializer):
        super().__init__()
        self._q = q
        self._fs = file_saver
        self._serializer = serializer

    def run(self):
        with self._fs as fs:
            while True:
                obj: str = self._q.get()
                if obj == FINISH_OBJECT:
                    return
                fs.save(self._serializer.serialize(obj))

