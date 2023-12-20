#encoding:utf-8
from django import forms
from .models import Anime

class UsuarioBusquedaForm(forms.Form):
    idUsuario = forms.IntegerField(label='IdUsuario')
    genero = forms.ChoiceField(choices=[], label='Género')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recuperar la lista de géneros y configurar las opciones del campo 'genero'
        generos = Anime.objects.values_list('generos', flat=True).distinct()
        generos_separados = set()
        for g in generos:
            splitted = g.split(',')
            for s in splitted:
                generos_separados.add(s.strip())
        self.fields['genero'].choices = [(g, g) for g in generos_separados]
