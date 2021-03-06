import os
import boto3
from botocore.exceptions import ClientError
from enum import Enum
import tempfile
import json
import logging

logger = logging.getLogger(__name__)

# TODO: only create this if needed. E.g. init to None, then later, create if None
store_s3 = None


class Storage_type(Enum):
    local_temp = 1  # e.g. /tmp
    s3 = 2          # AWS S3 bucket
    local_dev = 3   # e.g. working_dir/resources/texts


# TODO: change name to Files
class files(object):
    """Reads/writes text files to local directory or to S3 buckets"""

    def __init__(self, storage_type=Storage_type.local_temp):
        global store_s3
        self._storage_type = storage_type
        if storage_type == Storage_type.s3:
            if store_s3 is None:
                print("Initializing boto3/s3 client")
                store_s3 = boto3.client('s3')  # init boto3 client
            self._client = store_s3

    def write_text(self, text, filename=None):
        switcher = {Storage_type.local_temp: files.write_local_temp,
                    Storage_type.s3: files.write_text_s3,
                    Storage_type.local_dev: files.write_local_dev}

        func = switcher.get(self._storage_type)
        return func(self, text, filename)

    def write_local_temp(self, text, filename):
        fp = tempfile.TemporaryFile()
        fp.write(text.encode("utf-8"))
        fp.seek(0)  # Reset file-pointer to start of file, ready for reading back in
        return fp

    def write_text_s3(self, obj, filename):
        """Writes a text file to the parsed-texts S3 bucket"""
        self.write_s3(obj, "dcorney.com.text", filename)

    def write_s3(self, obj, bucket, s3_filename):
        """Write object to local temporary file, then upload to given bucket/filename """
        (fd, pathname) = tempfile.mkstemp()
        try:
            tfile = os.fdopen(fd, "w")
            json.dump(obj, tfile)
            tfile.close()

            logger.info("Dumped to temp file {}, ready to upload to S3".format(pathname))
            try:
                logger.info("Uploading to S3: {} / {} via {} ...".format(bucket, s3_filename, pathname))
                self._client.upload_file(pathname, bucket, "gut/{}".format(s3_filename))
            except:
                logger.error("Error uploading to S3: {} / {} via {} ...".format(bucket, s3_filename, pathname))
                raise
        finally:
            os.remove(pathname)
        return 1

    def read_text_s3(self, s3_filename):
        return(self.read_s3("dcorney.com.text", s3_filename))

    def read_s3(self, bucket, s3_filename):
        # client = boto3.client('s3')
        # bucket = 'parsed-texts'
        (fd, pathname) = tempfile.mkstemp()
        try:
            tfile = os.fdopen(fd, "wt")
            self._client.download_file(bucket, "gut/{}".format(s3_filename), pathname)
            with open(pathname) as json_data:
                obj = json.load(json_data)
            tfile.close()

        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object {} / {} does not exist.".format(bucket, s3_filename))
                obj = None
            else:
                raise
        finally:
            os.remove(pathname)
        return obj

    def write_local_dev(self, text, filename):
        file_dir = os.path.dirname(os.path.realpath(__file__)) + "/resources/texts/"
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        print("Writing to " + file_dir)
        f = open(file_dir + "/" + filename, 'w+b')
        f.write(text.encode("utf-8"))
        f.close()

    def redis_to_s3(self, redis_file="/usr/local/var/db/redis/dump.rdb"):
        redis_gz = "/usr/local/var/db/redis/dump.rdb.gz"  # TODO: zip into tmp directory
        with open(redis_file, 'rb') as f_in:
            with gzip.open(redis_gz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        bucket = "dcorney.com.redis-dumps"
        s3_filename = "redis_backup.rdb.gz"
        logger.info("Uploading redis backup to S3: {} / {} via {} ...".format(bucket, s3_filename, redis_gz))
        self._client.upload_file(redis_gz, bucket, "{}".format(s3_filename))

    def redis_from_s3(self, local_file="/usr/local/var/db/redis/dump.rdb"):
        # redis_gz = "/usr/local/var/db/redis/dump.rdb.gz" # TODO: zip into tmp directory
        bucket = "dcorney.com.redis-dumps"
        s3_filename = "redis_backup.rdb.gz"
        local_gz = "/usr/local/var/db/redis/dump.rdb.gz"
        logger.info("Downloading redis backup from S3: {} / {} to {} ...".format(bucket, s3_filename, local_gz))
        self._client.download_file(bucket, s3_filename, "{}".format(local_gz))
        with gzip.open(local_gz, 'rb') as f_in:
            with open(local_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


def dev():
    # F = files(Storage_type.local_temp)
    # file = F.write_text("this is a short bit of text", "dc_temp_file.txt")
    # print(file.read())
    f = files(Storage_type.s3)
    # f.redis_to_s3()
    f.redis_from_s3(local_file="/usr/local/var/db/redis/dump.rdb")
