from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


swagger_urls = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


# app urls
urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("events/", include("event.urls")),
] + swagger_urls
