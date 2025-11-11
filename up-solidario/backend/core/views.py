# backend/core/views.py
from django.shortcuts import render

def index(request):
    """ Esta view renderiza a nossa página principal, o index.html. """
    return render(request, 'index.html')