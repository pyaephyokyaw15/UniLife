from drf_extra_fields.fields import Base64ImageField

class CustomBase64ImageFiled(Base64ImageField):
    """
    To show Base64 Field on Swagger UI.

    # issues with drf-extra-fields
    #https://pypi.org/project/drf-yasg/#toc-entry-23
    """

    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'title': 'File Content',
            'description': 'Content of the file base64 encoded',
            'read_only': False  # <-- FIX
        }
