from django.contrib import admin
from .models import PropertySummary

class PropertySummaryAdmin(admin.ModelAdmin):
    list_display = ('property', 'summary', 'created_at', 'updated_at')
    search_fields = ('property__title', 'summary')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(PropertySummary, PropertySummaryAdmin)
