from django.contrib import admin
from bot.models import Rates

@admin.register(Rates)
class Ratesdmin(admin.ModelAdmin):
    pass
