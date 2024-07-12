# app/utils/s3_utils.py

import boto3
import os


class S3Utils:
    def __init__(self, region_name='us-east-1'):
        self.s3 = boto3.client('s3', region_name=region_name)

    def upload_file_to_s3(self, file_path, bucket_name, s3_key=None):
        if not s3_key:
            s3_key = os.path.basename(file_path)
        try:
            self.s3.upload_file(file_path, bucket_name, s3_key)
            return f"File uploaded to S3: s3://{bucket_name}/{s3_key}"
        except Exception as e:
            return f"Error uploading file to S3: {str(e)}"

    def upload_content_to_s3(self, content, bucket_name, s3_key):
        try:
            self.s3.put_object(Bucket=bucket_name, Key=s3_key, Body=content)
            return f"Content uploaded to S3: s3://{bucket_name}/{s3_key}"
        except Exception as e:
            return f"Error uploading content to S3: {str(e)}"

    def upload_parsed_content(self, file_path, text_key, tables_key, bucket_name):
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            text, tables = content.split("\n\n", 1)
            text_upload_result = self.upload_content_to_s3(text, bucket_name, text_key)
            tables_upload_result = self.upload_content_to_s3(tables, bucket_name, tables_key)

            return text_upload_result, tables_upload_result
        except Exception as e:
            return f"Error uploading parsed content to S3: {str(e)}"