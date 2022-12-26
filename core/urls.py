from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # authentications
    path('', include("accounts.urls"), name='authentications'),

    # posts
    path('', include("posts.urls"), name='posts'),

    # communities
    path('', include("community.urls"), name='communities'),

    # chat
    path('', include("chat.urls"), name='chat'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
