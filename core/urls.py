from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .consumer import ChatConsumer, NotificationConsumer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("documents.urls")),
    path("", include("chats.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    path("ws/chat/<str:document_id>/", ChatConsumer.as_asgi()),
]
