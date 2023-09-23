"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.v1.views import UserViewSet, RetrieveListProductViewSet
from djoser.views import TokenCreateView, TokenDestroyView

router = DefaultRouter()
router.register(
    r"users", UserViewSet, basename="users",
)
router.register(
    r"products", RetrieveListProductViewSet, basename="products",
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", TokenCreateView.as_view()),
    path("auth/logout/", TokenDestroyView.as_view()),
]
