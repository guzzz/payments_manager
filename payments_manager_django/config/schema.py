from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="Payments Manager API",
        default_version="v1",
        description="API that allows us to register and manage accounts and payments.",
        terms_of_service="",
        contact=openapi.Contact(email="email@email.com.br"),
        license=openapi.License(name="Test License"),
    ),
    validators=["flex", "ssv"],
    public=True,
)
