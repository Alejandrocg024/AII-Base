"""
URL configuration for practica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
import django.views
from main import views
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index),
    path('index.html/', views.index),
    path('populate/', views.cargar),
    path('loadRS/', views.loadRS),
    path('admin/',admin.site.urls),
    path('animes_por_formato/',views.anime_por_formato, name='anime_por_formato'),
    path('animes_mas_vistos/',views.animes_mas_vistos, name='animes_mas_vistos'),
    path('recomendar_animes/',views.recomendar_animes, name='recomendar_animes'),
]
