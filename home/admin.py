from django.contrib import admin

from models import Latest, DisplayAdvert


class LatestAdmin(admin.ModelAdmin):
    list_filter = ('created', 'title', 'body')
    list_display = ('title', 'created',)
    search_fields = ('created', 'title', 'body')
    date_hierarchy = 'created'
    ordering = ('created', 'created')
admin.site.register(Latest, LatestAdmin)


class DisplayAdmin(admin.ModelAdmin):
    list_filter = ('title', 'body')
    list_display = ('title', 'body',)
    search_fields = ('title', 'body')
admin.site.register(DisplayAdvert, DisplayAdmin)
