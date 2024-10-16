from django.urls import path
from .consumers import ChatApp,ChatSender,ChatGroup

websocket_urlpatterns = [
    path('ws/chat/<id>/<username>/',ChatApp.as_asgi()),
    path('ws/chat/<id1>/<username1>/<id2>/<username2>/',ChatSender.as_asgi()),
    path('ws/Home/<id>/<username>/<groupname>/',ChatGroup.as_asgi()),
]