"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

api_v1 = 'api/v1/'


schema_view = get_schema_view(
    openapi.Info(
        title="YFinance API",
        default_version='v1',
        description="API для оборачивания функционала yfinance",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


admin_urlpatterns = [
    path('admin/', admin.site.urls),
]

apps_urlpatterns = [
    path(f'{api_v1}tickers/', include('apps.tickers.urls')),
    path(f'{api_v1}financials/', include('apps.financials.urls')),
    path(f'{api_v1}options/', include('apps.options.urls')),
    # Пути для документации:
]
docs_urlpatterns = [
    path("", include("utils.docs")),
]

urlpatterns = [
    *admin_urlpatterns,
    *apps_urlpatterns,
    *docs_urlpatterns,
]
