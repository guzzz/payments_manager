from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action

from .producer import publish
from .filters import TransactionFilter
from .models import Account, Transaction
from .filter_backends import TransactionFilterBackend
from .serializers import (
    AccountSerializer,
    TransactionSerializer,
    AccountPartialUpdateSerializer,
)


class AccountViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Account.objects.all()
    serializer = AccountSerializer

    def get_serializer_class(self):
        if self.action == "update":
            return AccountPartialUpdateSerializer
        else:
            return AccountSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish("account_created", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=True)
    def balance(self, request, pk=None):
        account = get_object_or_404(Account, id=pk)
        balance = "{:.2f}".format(account.balance)
        response = {"balance": balance}
        return Response(response, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def activate(self, request, pk=None):
        return self.update_active_flag(pk, True)

    @action(methods=["get"], detail=True)
    def inactivate(self, request, pk=None):
        return self.update_active_flag(pk, False)

    def update_active_flag(self, pk, active_flag):
        account = get_object_or_404(Account, id=pk)
        account.active = active_flag
        account.save()

        account_updated = {"account_id": account.id, "active_flag": account.active}
        publish("account_active_flag_updated", account_updated)

        response = {"message": "Success!"}
        return Response(response, status=status.HTTP_200_OK)


class TransactionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_class = TransactionFilter
    filter_backends = (TransactionFilterBackend,)

    def get_queryset(self):
        account = get_object_or_404(Account, id=self.kwargs["account_id"])
        queryset = self.queryset.filter(account__id=account.id)
        return queryset
