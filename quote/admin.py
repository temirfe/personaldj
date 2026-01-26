from django.contrib import admin
from .models import Quote
from django.utils.html import format_html

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('truncated_body', 'author')
    def truncated_body(self, obj):
        return format_html('{}...', obj.body[:50])
    truncated_body.short_description = 'Quote' 

admin.site.register(Quote, QuoteAdmin)
