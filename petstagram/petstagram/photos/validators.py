from django.core.exceptions import ValidationError

from petstagram.core.utils import megabytes_to_bytes


def validate_file_less_than_5mb(fileobj):
    filesize = fileobj.file.size
    megabyte_limit = 5
    if filesize > megabytes_to_bytes(filesize):
        raise ValidationError(f"Max file size is {megabyte_limit}MB")
