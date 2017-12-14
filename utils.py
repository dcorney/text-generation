import os
import boto3
import botocore
import logging

ner_per = "PERSON"
ner_org = "ORGANIZATION"
ner_loc = "LOCATION"
START_TOKEN = "<START_TOKEN>"
END_TOKEN = "<END_TOKEN>"
S3_RESOURCE_BUCKET = "dcorney.com.textgen.resources"

logger = logging.getLogger(__name__)


# #Not used?!
# def s3_download(s3_bucket, s3_file_path, local_file_path, aws_profile='default'):
#     '''
#     Downloads an object from the signalml S3 bucket given a path to the S3 object
#     and file name to save as.
#     e.g. s3_file_path: path/to/s3/file
#          local_file_path:    path/to/destination
#     '''

#     if os.path.exists(local_file_path):
#         logger.info("Found local copy of '%s'" % local_file_path)
#     else:
#         dir_name = os.path.dirname(local_file_path)
#         os.makedirs(dir_name, exist_ok=True)
#         session = boto3.Session(profile_name=aws_profile)
#         client = session.client('s3')
#         s3_path = 's3://{}/{}'.format(s3_bucket, s3_file_path)
#         try:
#             logger.info("Downloading from S3: %s ..." % s3_path)
#             client.download_file(s3_bucket, s3_file_path, local_file_path)
#             logger.info('Saved to %s' % local_file_path)
#         except botocore.exceptions.ClientError as e:
#             logger.info("Could not find file at '%s'" % s3_path)
#             logger.info(e)
#             raise
