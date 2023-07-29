from django.contrib import messages
from django.shortcuts import render


def index(request):
    return render(request, 'core_templates/index.html')
