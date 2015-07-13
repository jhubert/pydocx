# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from unittest import TestCase
from pydocx.test.utils import get_img_fixture
from pydocx.export.image_upload import S3ImageUploader
import json
from pydocx.exceptions import ImageUploadException


class S3ImageUploaderTestCase(TestCase):
    def test_input_as_json(self):
        signed_request = get_img_fixture('upload_signed_request.json', as_binary=True)

        s3 = S3ImageUploader(signed_request)

        self.assertIsInstance(s3.signed_data, dict)

    def test_input_as_dict(self):
        signed_request = get_img_fixture('upload_signed_request.json', as_binary=True)
        signed_request = json.loads(signed_request)

        s3 = S3ImageUploader(signed_request)

        self.assertIsInstance(s3.signed_data, dict)

    def test_image_extension_from_filename(self):
        signed_request = get_img_fixture('upload_signed_request.json', as_binary=True)

        s3 = S3ImageUploader(signed_request)

        image_format = s3.get_image_format('image1.png')

        self.assertEqual('png', image_format)

    def test_upload_image(self):
        signed_request = get_img_fixture('upload_signed_request.json', as_binary=True)
        signed_request = json.loads(signed_request)

        s3 = S3ImageUploader(signed_request)

        img_data = get_img_fixture('image1.png', as_binary=True)

        result = s3.upload(img_data, 'image2.png', 'png')

        self.assertEqual('http://pydocx.s3.amazonaws.com/uploads/pydocx/image2.png', result)

    def test_upload_image_invalid_url(self):
        signed_request = get_img_fixture('upload_signed_request.json', as_binary=True)
        signed_request = json.loads(signed_request)

        signed_request['url'] = 'http://invalid_bucket.s3.amazonaws.com/'

        s3 = S3ImageUploader(signed_request)

        img_data = get_img_fixture('image1.png', as_binary=True)

        self.assertRaises(ImageUploadException, s3.upload, img_data, 'image2.png', 'png')

    def test_upload_image_invalid_signed_request(self):
        signed_request = get_img_fixture('upload_signed_request.json', as_binary=True)
        signed_request = json.loads(signed_request)

        signed_request['AWSAccessKeyId'] += 'test'

        s3 = S3ImageUploader(signed_request)

        img_data = get_img_fixture('image1.png', as_binary=True)

        self.assertRaises(ImageUploadException, s3.upload, img_data, 'image3.png', 'png')

    def test_upload_image_as_data(self):
        signed_request = get_img_fixture('upload_signed_request.json', as_binary=True)
        signed_request = json.loads(signed_request)

        s3 = S3ImageUploader(signed_request)

        img_data = get_img_fixture('image1.data', as_binary=True)

        result = s3.upload(img_data, 'image4.jpg')

        self.assertEqual('http://pydocx.s3.amazonaws.com/uploads/pydocx/image4.jpg', result)
