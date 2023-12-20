#encoding:utf-8

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User 

'''
(1 punto) CONSTRUIR UN MODELO DE DATOS CORRECTO en Django que almacene la
información siguiente:
a) Pelicula: idPelicula, Título, Director, idIMDB y Géneros
b) Puntuación: IdUsario, idPelicula, Puntuación (10-50, en rangos de 5) 

'''


class Generos(models.Model):
    idGeneros = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30, verbose_name='Generos')

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering =('nombre', )

class Pelicula(models.Model):
    idPelicula = models.IntegerField(primary_key=True)
    titulo = models.TextField(verbose_name='Título')
    director = models.CharField(verbose_name='Director', max_length=30)
    idIMDB = models.CharField(max_length=30, verbose_name='idIMDB')
    generos = models.ManyToManyField(Generos)
    puntuaciones = models.ManyToManyField(User, through='Puntuacion')

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ('titulo', 'director', )

class Puntuacion(models.Model):
    PUNTUACIONES = ((10, '10'), (15, '15'), (20, '20'), (25, '25'), (30, '30'), (35, '35'), (40, '40'), (45, '45'), (50, '50'))
    idUsuario = models.ForeignKey(User,on_delete=models.CASCADE)
    idPelicula = models.ForeignKey(Pelicula,on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField(verbose_name='Puntuación', validators=[MinValueValidator(10), MaxValueValidator(50)], choices=PUNTUACIONES)
    
    def __str__(self):
        return (str(self.puntuacion))
    
    class Meta:
        ordering=('idPelicula','idUsuario', )