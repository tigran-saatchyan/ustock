"""OpenAPI documentation for the UStock API.

This module configures the OpenAPI schema generation using drf_yasg and defines
URL patterns for the API documentation interfaces:
  - JSON schema (without UI)
  - Swagger UI
  - ReDoc UI

The generated schema provides detailed API information including title, version,
description, terms of service, contact and license information.
"""

from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="UStock API",
        default_version="v1.0",
        description=(
            "UStock API provides full access to financial data wrapped with the functionality "
            "of the yFinance library. The service includes retrieving ticker information, historical quotes, "
            "dividends, splits, analyst recommendations, event calendars, ESG data, financial statements (balance sheet, "
            "income statement, cash flow), and option chains. This API allows integration of data for analysis and the "
            "development of financial applications."
        ),
        terms_of_service="https://github.com/tigran-saatchyan/UStock/blob/master/TERMS_OF_SERVICE",
        contact=openapi.Contact(
            email="mr.saatchyan@yandex.com",
            name="Tigran Saatchyan",
            url="https://github.com/tigran-saatchyan",
        ),
        license=openapi.License(
            name="MIT License",
            url="https://github.com/tigran-saatchyan/UStock/blob/master/LICENSE.md",
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Endpoint for JSON schema without a UI: e.g. /swagger.json or /swagger.yaml
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    # Endpoint for Swagger UI: displays interactive API documentation.
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # Endpoint for ReDoc UI: alternative API documentation interface.
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
