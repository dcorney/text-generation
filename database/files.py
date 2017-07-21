import os
from enum import Enum
import logging
import tempfile

logger = logging.getLogger(__name__)

# TODO : Write the read functions!

class Storage_type(Enum):
    local_temp = 1  # e.g. /tmp
    s3 = 2          # AWS S3 bucket
    local_dev = 3   # e.g. working_dir/resources/texts


class files(object):
    """Reads/writes text files to local directory or to S3 buckets"""
    def __init__(self, storage_type=Storage_type.local_temp):
        self._storage_type = storage_type

    def write_text(self, text, filename=None):
        switcher = {Storage_type.local_temp: files.write_local_temp,
                    Storage_type.s3: files.write_s3,
                    Storage_type.local_dev: files.write_local_dev}

        func = switcher.get(self._storage_type)
        return func(self, text, filename)

    def write_local_temp(self, text, filename):
        fp = tempfile.TemporaryFile()
        fp.write(text.encode("utf-8"))
        fp.seek(0)  # Reset file-pointer to start of file, ready for reading back in
        return fp

    def write_s3(self, text, filename):
        # TODO: write
        return 0

    def write_local_dev(self, text, filename):
        file_dir = os.path.dirname(os.path.realpath(__file__)) + "/resources/texts"
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = open(file_dir + "/" + filename, 'w+b')
        f.write(text.encode("utf-8"))
        f.close()


def dev():
    F = files(Storage_type.local_temp)
    file = F.write_text("this is a short bit of text", "dc_temp_file.txt")
    print(file.read())


if __name__ == '__main__':
    test()
