from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls"), name="users"),
    path("notes/", include("notes.urls"), name="notes"),
]
