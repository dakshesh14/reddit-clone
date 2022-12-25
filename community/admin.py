from django.contrib import admin

from .models import Community, JoinedCommunity


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass


@admin.register(JoinedCommunity)
class JoinedCommunityAdmin(admin.ModelAdmin):
    pass
