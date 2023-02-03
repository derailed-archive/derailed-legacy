"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
"""
import base64
import os
import aioboto3
from fastapi import HTTPException


S3_URI = os.environ['S3_URI']
S3_KEY_ID = os.environ['S3_KEY_ID']
S3_KEY_SECRET = os.environ['S3_KEY_SECRET']


def to_raw(data_type: str, data: str) -> bytes | None:
    if data_type == 'base64':
        return base64.b64decode(data)


def parse_data_uri(uri: str) -> tuple[str, bytes]:
    try:
        header, headered_data = uri.split(';')

        _, given_mime = header.split(':')
        data_type, data = headered_data.split(',')

        raw_data = to_raw(data_type, data)

        if raw_data is None:
            raise HTTPException(400, 'Unable to parse image data')

        return given_mime, raw_data
    except ValueError:
        raise HTTPException('Invalid data uri syntax')


class UploadManager:
    def __init__(self) -> None:
        self._session = aioboto3.Session(aws_access_key_id=S3_KEY_ID, aws_secret_access_key=S3_KEY_SECRET)


    async def upload(self, sf: int, bucket: str, file: bytes) -> None:
        snowflake = str(sf)

        client = self._session.resource('s3', endpoint_url=S3_URI)

        s3_bucket = await client.Bucket(bucket)

        await s3_bucket.put_object(Key=snowflake, Body=file)
