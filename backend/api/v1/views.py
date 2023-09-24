from typing import Optional, Type

from djoser import serializers
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.serializers import Serializer

from api.v1.serializers import (
    AllProductSerializer,
    ConcreteProductSerializer,
    StatProductSerializer,
)
from education.models import Product
from users.models import User


class MultiSerializerViewSetMixin:
    """Миксин для выбора нужного сериализатора из `serializer_classes`."""

    serializer_classes: Optional[dict[str, Type[Serializer]]] = None

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super().get_serializer_class()


class UserViewSet(
    MultiSerializerViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Кастомный вьюсет Djoser для работы с пользователями.

    Предоставляет пользователям возможность регистрации аккаунта,
    получения информации о себе/пользователях/пользователе,
    смены своего пароля, подписки/отписки на/от другого пользователя,
    просмотра своих подписок.
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    serializer_classes = {
        "create": serializers.UserCreateSerializer,
        "list": serializers.UserSerializer,
        "retrieve": serializers.UserSerializer,
        "me": serializers.UserSerializer,
        "get_all_products": AllProductSerializer,
        "get_concrete_product": ConcreteProductSerializer,
    }

    def get_queryset(self):
        if (
            self.action == "get_all_products"
            or self.action == "get_concrete_product"
        ):
            return self.request.user.user_products.all()
        return super().get_queryset()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_instance(self):
        return self.request.user

    @action(
        ["get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path="me",
    )
    def me(self, request, *args, **kwargs):
        """Функция-обработчик для эндпоинта "/users/me/".

        Позволяет пользователям получать информацию о себе.
        """
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(
        ["get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path="me/products",
        url_name="get_all_products",
    )
    def get_all_products(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(
        ["get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path=r"me/products/(?P<pk>\w+)",
        url_name="get_concrete_product",
    )
    def get_concrete_product(self, request, pk, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RetrieveListProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StatProductSerializer
