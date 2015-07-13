# coding: utf-8
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from pydocx.export.image_resize import (
    get_image_data_and_filename,
)

from pydocx.export.image_upload import S3ImageUploader
import time


class S3ImagesUploadMixin(object):
    def __init__(self, *args, **kwargs):
        s3_upload = kwargs.pop('s3_upload', None)
        self.unique_filename = kwargs.pop('unique_filename', True)

        super(S3ImagesUploadMixin, self).__init__(*args, **kwargs)

        self.image_uploader = S3ImageUploader(s3_upload)

    def image(self, image_data, filename, x, y, uri_is_external):
        if uri_is_external:
            image_data, filename = get_image_data_and_filename(
                image_data,
                filename,
            )

        if self.unique_filename:
            # make sure that the filename is unique so that it will not rewrite
            # existing images from s3
            filename = "%s-%s" % (str(time.time()).replace('.', ''), filename)

        s3_url = self.image_uploader.upload(image_data, filename)

        image_data = s3_url
        uri_is_external = True

        return super(S3ImagesUploadMixin, self).image(
            image_data,
            filename,
            x,
            y,
            uri_is_external
        )
