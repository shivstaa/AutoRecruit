from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'listen/(?P<session_id>[^/]+)/$', consumers.TranscriptConsumer.as_asgi()),
]
