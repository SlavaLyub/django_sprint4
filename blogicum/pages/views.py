from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


def page_not_found_view(request, exception):
    return render(request, 'pages/404.html', status=404)


def forbidden(request, exception):
    return render(request, 'pages/403csrf.html', status=403)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def call_500(request):
    return HttpResponse(status=500)


class AboutView(TemplateView):
    template = 'pages/about.html'


class RulesView(TemplateView):
    template = 'pages/rules.html'
