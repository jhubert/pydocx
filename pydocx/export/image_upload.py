# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

import json
import base64
from urlparse import urljoin
from collections import namedtuple
import os

import requests
from xml.etree import ElementTree

from pydocx.exceptions import ImageUploadException
from pydocx.util import uri


class ImageUploader(object):
    def upload(self, *args, **kwargs):
        raise NotImplemented()


class S3ImageUploader(ImageUploader):
    def __init__(self, signed_data):
        if isinstance(signed_data, basestring):
            signed_data = json.loads(signed_data)

        self.signed_data = signed_data

        self.OK_STATUS = 204
        self.S3_ERROR_STATUS = 403

    def _s3_url(self, bucket_name):
        return 'https://%s.s3.amazonaws.com/' % bucket_name

    def _prepare_s3_upload(self, filename):
        """Prepare all the data for uploading to s3. Also here we construct the final url of the
        image.
        """

        url = self.signed_data.pop('url', None)

        key_name = self.signed_data['key'].replace('${filename}', filename)

        policy_data = json.loads(base64.b64decode(self.signed_data['policy']))

        bucket_name = None

        for item in policy_data['conditions']:
            if isinstance(item, dict) and item.get('bucket', None):
                bucket_name = item['bucket']
                break

        if not url:
            url = self._s3_url(bucket_name)

        img_url = urljoin(url, key_name)

        s3 = namedtuple('S3Upload', 'url data img_url')

        return s3(url, self.signed_data, img_url)

    def get_image_format(self, filename):
        """Return the format based on extension"""

        return os.path.splitext(filename)[1].strip('.')

    def image_data_decode(self, image_data):
        """We can have image data in multiple formats: binary or as image data base64 encoded"""

        match = uri.is_encoded_image_uri(image_data)
        if match:
            image_data = base64.b64decode(match.group('image_data'))

        return image_data

    def upload(self, img_data, filename, image_format=None):
        """Upload image to amazon s3"""

        # make sure that we decode base64 encoded images
        img_data = self.image_data_decode(img_data)

        s3_obj = self._prepare_s3_upload(filename)

        data = s3_obj.data

        image_format = image_format or self.get_image_format(filename)

        data['Content-Type'] = 'image/%s' % image_format

        r = requests.post(s3_obj.url, data=data, files={'file': (filename, img_data)})

        if r.status_code == self.S3_ERROR_STATUS:
            error = ElementTree.fromstring(r.content)
            code = error.find("Code").text
            message = error.find("Message").text
            raise ImageUploadException("S3 {0} - {1}".format(code, message))
        elif r.status_code != self.OK_STATUS:
            raise ImageUploadException("S3 Upload Error: {0}".format(r.text))

        return s3_obj.img_url
