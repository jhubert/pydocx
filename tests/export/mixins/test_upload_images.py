# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from pydocx.export.html import PyDocXHTMLExporter
from pydocx.export.mixins.upload_images import S3ImagesUploadMixin
from pydocx.export.mixins.resized_images import ResizedImagesExportMixin
from unittest import TestCase
from pydocx.test.utils import get_img_fixture, assert_html_equal


class PyDocXHTMLExporterS3ImageUpload(
    S3ImagesUploadMixin,
    PyDocXHTMLExporter
):
    pass


class PyDocXHTMLExporterImageResizeS3ImageUpload(
    ResizedImagesExportMixin,
    S3ImagesUploadMixin,
    PyDocXHTMLExporter
):
    pass


class PyDocXHTMLExporterS3ImageUploadTestCase(TestCase):
    exporter = PyDocXHTMLExporterS3ImageUpload

    def test_export_docx_to_html_with_image_upload_to_s3(self):
        docx_file_path = get_img_fixture('png_basic_resize_linked_photo.docx')

        signed_request = get_img_fixture('upload_singed_request.json', as_binary=True)

        html_file_content = get_img_fixture(
            'png_basic_s3_upload.html',
            as_binary=True
        )

        html = self.exporter(docx_file_path, s3_upload=signed_request,
                             unique_filename=False).parsed

        assert_html_equal(html, html_file_content)


class PyDocXHTMLExporterImageResizeS3ImageUploadTestCase(TestCase):
    exporter = PyDocXHTMLExporterImageResizeS3ImageUpload

    def test_export_docx_resize_upload_to_s3(self):
        docx_file_path = get_img_fixture('png_basic_resize_linked_photo.docx')

        signed_request = get_img_fixture('upload_singed_request.json', as_binary=True)

        html_file_content = get_img_fixture(
            'png_basic_resize_and_s3_upload.html',
            as_binary=True
        )

        html = self.exporter(docx_file_path, s3_upload=signed_request,
                             unique_filename=False).parsed

        assert_html_equal(html, html_file_content)
