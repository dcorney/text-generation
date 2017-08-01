import os
import boto3
from enum import Enum
import tempfile
import json
import logging

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

    # def write_local_temp_obj(self, obj):
    #     fp = tempfile.TemporaryFile()
    #     fp.write(obj)
    #     fp.seek(0)  # Reset file-pointer to start of file, ready for reading back in
    #     return fp


    def write_s3(self, obj, filename):
        # dir_name = os.path.dirname(file_path)
        # os.makedirs(dir_name, exist_ok=True)
        tempfile = os.path.dirname(os.path.realpath(__file__)) + "/resources/temp.json"
        with open(tempfile, 'w') as fp:
            json.dump(obj, fp)

        #s3_path =  "/".join('s3:/','parsed-texts','gut',filename)  #os.environ['S3_BUCKET']
        client = boto3.client('s3')
        bucket = 'parsed-texts'
        #s3_path = 's3://{}/{}'.format(bucket, s3_file_path)
        try:
            print("Uploading to S3: {} / {} ...".format(bucket, filename) )
            client.upload_file(tempfile, bucket, "gut/" + filename)
            
        except:
            print("Error writing to S3")
            raise
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
