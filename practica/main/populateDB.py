from datetime import datetime
from .models import Anime, Puntuacion

path = "data"

def load_animes():
    with open(path + "/anime.txt", "r") as f:
        next(f)
        fLines = f.readlines()
        for line in fLines:
            datatoLoad = line.split("\t")
            animeId, titulo, generos, formato, numEpisodios = datatoLoad

            numEpisodios = numEpisodios if numEpisodios != 'Unknown\n' else None

            Anime.objects.create(animeId=animeId, titulo=titulo, generos=generos, formato=formato, numEpisodios=numEpisodios)

def load_puntuaciones():
    with open(path + "/ratings.txt", "r") as f:
        next(f)
        fLines = f.readlines()
        for line in fLines:
            dataToLoad = line.split("\t")
            idUsuario, animeId, puntuacion = dataToLoad

            try:
                Puntuacion.objects.create(idUsuario=idUsuario, animeId=Anime.objects.get(animeId=animeId), puntuacion=puntuacion)
            except:
                print("Error al cargar la puntuacion: " + str(dataToLoad) + " para el anime: " + str(animeId))

def delete_database():
    Anime.objects.all().delete()
    Puntuacion.objects.all().delete()

def populate():
    delete_database()
    load_animes()
    load_puntuaciones()