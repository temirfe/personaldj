from django.shortcuts import render
from django.views import generic
from .models import Quote

# Create your views here.
class QuoteList(generic.ListView):
    model = Quote
    #template_name = 'quote/quote_list.html'

class QuoteDetail(generic.DetailView):
    model = Quote
    #template_name = 'quote/quote_detail.html'