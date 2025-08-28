from django.urls import include, path
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("dispatch/", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
