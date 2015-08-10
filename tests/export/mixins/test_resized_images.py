# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from pydocx.export.html import PyDocXHTMLExporter
from pydocx.export.mixins import ResizedImagesExportMixin
from unittest import TestCase
from pydocx.test import utils


class PyDocXHTMLExporterWithResizedImages(
    ResizedImagesExportMixin,
    PyDocXHTMLExporter
):
    pass


class PyDocXHTMLExporterWithResizedImagesTestCase(TestCase):
    exporter = PyDocXHTMLExporterWithResizedImages

    def test_export_docx_to_resized_images(self):
        docx_file_path = utils.get_img_fixture('png_basic_resize_linked_photo.docx')
        html_file_content = utils.get_img_fixture(
            'png_basic_resize_linked_photo.html',
            as_binary=True
        )

        html = self.exporter(docx_file_path).parsed

        utils.assert_html_equal(html, html_file_content)

    def test_export_docx_to_resized_images_invalid_input_image_and_skip(self):
        docx_file_path = utils.get_img_fixture('invalid_image_error.docx')

        html_file_content = utils.get_img_fixture(
            'invalid_image_error.html',
            as_binary=True
        )

        html = self.exporter(docx_file_path).parsed

        utils.assert_html_equal(html, html_file_content)
