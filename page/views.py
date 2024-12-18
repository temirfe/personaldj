from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    """ template = loader.get_template("page/home.html")
    context = {
        "yoba": 'nahoi',
    }
    return HttpResponse(template.render(context, request)) """
    context = {"yoba": "nahoi"}
    return render(request, "page/home.html", context)
