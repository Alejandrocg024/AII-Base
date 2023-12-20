#encoding:utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponseRedirect
from django.conf import settings
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
import shelve
from main.populateDB import populate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from gevent.libev.corecext import NONE


def cargar(request):
    if request.method == 'POST':
        if 'confirmar' in request.POST:
            populate()
            return redirect('/')

    return render(request, 'populate.html')


def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})

