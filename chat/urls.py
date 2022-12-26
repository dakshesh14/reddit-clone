from django.urls import path, include

urlpatterns = [
    path('api/chat/', include('chat.api.urls'), name='community-chat-api'),
]
