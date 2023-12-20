#encoding:utf-8
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, HttpResponse

#muestra una pantalla con el título del proyecto. Es un html estático
def sobre(request):
    html="<html><body>Proyecto de ejemplo de vistas</body></htm>"
    return HttpResponse(html)