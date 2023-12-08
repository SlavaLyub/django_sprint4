from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template = 'pages/about.html'


class RulesView(TemplateView):
    template = 'pages/rules.html'
