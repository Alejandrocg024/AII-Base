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
from main.forms import UsuarioBusquedaForm

def cargar(request):
    if request.method == 'POST':
        if 'confirmar' in request.POST:
            populate()
            return redirect('/')

    return render(request, 'populate.html')

'''
d) (1.75 puntos) ANIMES MÁS VISTOS. Muestre los tres animes con más puntuaciones
(Título y número de puntuaciones). Para cada uno de ellos mostrar también los dos animes
que más se le parecen (Título y similitud). 
'''

def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.idUsuario)
        itemid = int(ra.animeId.animeId)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

def loadRS(request):
    loadDict()
    return HttpResponseRedirect('/index.html')

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


def anime_por_formato(request):
    formatos = Anime.objects.values_list('formato', flat=True).distinct()
    formatos_separados = []

    for g in formatos:
        l = g.split(',')
        for s in l:
            if s not in formatos_separados:
                formatos_separados.append(s)

    generos = formatos_separados

    if request.method == 'POST':
        selected_formato = request.POST.get('formato')
        animes_formato = Anime.objects.filter(formato__contains=selected_formato, numEpisodios__gt=5).order_by('numEpisodios')
        
        return render(request, 'anime_por_formato.html', {'animes_formato': animes_formato})

    return render(request, 'anime_por_formato.html', {'generos': generos})


def recomendar_animes_genero_usuario_RSitems(request):
    formulario = UsuarioBusquedaForm()
    items = None

    if request.method == 'POST':
        formulario = UsuarioBusquedaForm(request.POST)
        
        if formulario.is_valid():
            idUsuario = formulario.cleaned_data['idUsuario']
            genero = formulario.cleaned_data['genero']

            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()

            rankings = getRecommendedItems(Prefs, SimItems, int(idUsuario))

            animes_recomendados = [(Anime.objects.get(pk=re[1]), re[0]) for re in rankings if genero in Anime.objects.get(pk=re[1]).generos]

            animes_filtrados = sorted(animes_recomendados, key=lambda x: x[1], reverse=True)[:2]

            items = animes_filtrados

    return render(request, 'recomendar_animes_usuarios.html', {'formulario': formulario, 'items': items})

def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})



