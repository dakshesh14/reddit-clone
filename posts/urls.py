from django.urls import path, include

urlpatterns = [
    path('api/', include('posts.api.urls'), name='posts-api'),
]
