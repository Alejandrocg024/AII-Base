#encoding:utf-8

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

'''
(1 punto) CONSTRUIR UN MODELO DE DATOS CORRECTO en Django que almacene la
información siguiente:
a) Anime: Animeid, Título, Géneros, Formato de emisión (TV, movie,…), Número de
episodios.
b) Puntuación: IdUsario, Animeid, Puntuación (1-10) 

'''


class Anime(models.Model):
    animeId = models.IntegerField(primary_key=True, default=0)
    titulo = models.CharField(max_length=255)
    generos = models.CharField(max_length=255, verbose_name='Generos')
    formato = models.CharField(max_length=50)
    numEpisodios = models.IntegerField()

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering =('titulo', )

class Puntuacion(models.Model):
    idUsuario = models.IntegerField()
    animeId = models.ForeignKey(Anime, on_delete=models.CASCADE, default=0)
    puntuacion = models.IntegerField(verbose_name='Puntuación',validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ('animeId', 'puntuacion', )