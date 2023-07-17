from django.contrib import admin
from .models import Ad


class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'city', 'category', 'phone', 'author')


admin.site.register(Ad, AdAdmin)
