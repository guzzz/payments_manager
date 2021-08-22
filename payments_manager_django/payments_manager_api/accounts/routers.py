from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"accounts", views.AccountViewSet)
router.register(r"extract/(?P<account_id>[^/.])", views.TransactionViewSet)
