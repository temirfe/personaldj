from django.urls import path

from . import views

app_name = 'quote'
urlpatterns = [
    path('',views.QuoteList.as_view(), name = 'index'),
    path('<int:pk>',views.QuoteDetail.as_view(), name = 'detail')
]
