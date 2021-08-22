import coreapi
import coreschema

from django_filters.rest_framework import DjangoFilterBackend


class CustomFilterBackend(DjangoFilterBackend):
    """
    Custom filter to insert a query_param
    """

    def get_schema_fields(self, view):
        fields = super(CustomFilterBackend, self).get_schema_fields(view)
        return fields


class TransactionFilterBackend(CustomFilterBackend):
    def get_schema_fields(self, view):
        fields = super(TransactionFilterBackend, self).get_schema_fields(view)
        extra_fields = [
            coreapi.Field(
                name="created_before",
                location="query",
                required=False,
                schema=coreschema.Object(),
            ),
            coreapi.Field(
                name="created_after",
                location="query",
                required=False,
                schema=coreschema.Object(),
            ),
        ]
        fields.extend(extra_fields)
        return fields
