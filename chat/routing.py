# # mysite/routing.py
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import chat.routing
# from django.conf.urls import url
# from . import consumers
#
# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })
# websocket_urlpatterns = [
#     url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
# ]