from django.urls import path, include

urlpatterns = [
    path('api/', include('community.api.urls'), name='community-api'),
]
