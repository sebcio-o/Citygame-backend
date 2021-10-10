from django.shortcuts import render
from django.views import generic
from core.models import Report


class DashboardView(generic.ListView):
    template_name = "dashboard.html"
    model = Report
