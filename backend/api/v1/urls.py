from djoser.views import TokenCreateView, TokenDestroyView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.v1.views import RetrieveListProductViewSet, UserViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="Education API",
        default_version="v1",
        description="123",
        contact=openapi.Contact(url="https://t.me/kritohanzo"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


router = DefaultRouter()
router.register(
    r"users",
    UserViewSet,
    basename="users",
)
router.register(
    r"products",
    RetrieveListProductViewSet,
    basename="products",
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", TokenCreateView.as_view()),
    path("auth/logout/", TokenDestroyView.as_view()),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
