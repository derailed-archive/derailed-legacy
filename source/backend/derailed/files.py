"""
Copyright (C) 2021-2023 Derailed

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
