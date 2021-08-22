from django.contrib import admin
from django.urls import path, include, re_path

from payments_manager_api.accounts.routers import router as accounts_router
from payments_manager_api.persons.routers import router as persons_router

from .schema import schema_view


urlpatterns = [
    re_path(
        r"^$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"
    ),
    path("admin/", admin.site.urls),
    path("", include(accounts_router.urls)),
    path("", include(persons_router.urls)),
]
