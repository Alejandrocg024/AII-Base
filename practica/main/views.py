#encoding:utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponseRedirect
from django.conf import settings
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
import shelve
from main.models import Anime, Puntuacion
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

    return render(request, 'populate.html',{'STATIC_URL':settings.STATIC_URL})

'''
d) (1.75 puntos) ANIMES MÁS VISTOS. Muestre los tres animes con más puntuaciones
(Título y número de puntuaciones). Para cada uno de ellos mostrar también los dos animes
que más se le parecen (Título y similitud). 
'''
def animes_mas_vistos(request):
    animes_mas_vistos = get_list_or_404 = (Anime.objects.all().order_by('-numPuntuaciones'))[:3]
    animes_final = {}
    for anime in animes_mas_vistos:
        idAnime = anime.idAnime
        shelf = shelve.open("dataRS.dat")
        ItemsPrefs = shelf['ItemsPrefs']
        shelf.close()
        parecidas = topMatches(ItemsPrefs, int(idAnime),n=3)
        animes = []
        similaridad = []
        for re in parecidas:
            animes.append(Anime.objects.get(pk=re[1]))
            similaridad.append(re[0])
        items= zip(animes,similaridad)
        animes_final[anime] = items
    
    return render(request, 'animes_mas_vistos.html', {'animes': animes_final, 'STATIC_URL':settings.STATIC_URL})


def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})



