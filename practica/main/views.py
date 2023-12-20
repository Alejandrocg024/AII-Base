#encoding:utf-8
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from gevent.libev.corecext import NONE


#Funcion de acceso restringido que carga los datos en la BD  
@login_required(login_url='/ingresar')
def populateDatabase(request):
    populate()
    logout(request)  # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    return HttpResponseRedirect('/index.html')


def loadRS(request):
    loadDict()
    return HttpResponseRedirect('/index.html')





def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})


def ingresar(request):
    formulario = AuthenticationForm()
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario=request.POST['username']
        clave=request.POST['password']
        acceso=authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate'))
            else:
                return render(request, 'mensaje_error.html',{'error':"USUARIO NO ACTIVO",'STATIC_URL':settings.STATIC_URL})
        else:
            return render(request, 'mensaje_error.html',{'error':"USUARIO O CONTRASEÑA INCORRECTOS",'STATIC_URL':settings.STATIC_URL})
                     
    return render(request, 'ingresar.html', {'formulario':formulario, 'STATIC_URL':settings.STATIC_URL})


