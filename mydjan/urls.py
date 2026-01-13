from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('',include('page.urls')),
    path('admin/', admin.site.urls),
    path('quote/',include('quote.urls')),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
