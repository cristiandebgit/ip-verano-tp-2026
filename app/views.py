# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')
#4ta función invoco services.py para traer las imagenes
def home(request):
    """
    Vista principal que muestra la galería de personajes de Los Simpsons.
    
    Esta función debe obtener el listado de imágenes desde la capa de servicios
    y también el listado de favoritos del usuario, para luego enviarlo al template 'home.html'.
    Recordar que los listados deben pasarse en el contexto con las claves 'images' y 'favourite_list'.
    images = []
    favourite_list = []
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    """
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)
    #convierto la lista de favoritos en nombres
    favourite_names = [fav.name for fav in favourite_list]

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list,
        'favourite_names': favourite_names
    })
#5ta función invoco services.py para realizar la busqueda de personajes
def search(request):
    """
    Busca personajes por nombre.
    
    Se debe implementar la búsqueda de personajes según el nombre ingresado.
    Se debe obtener el parámetro 'query' desde el POST, filtrar las imágenes según el nombre
    y renderizar 'home.html' con los resultados. Si no se ingresa nada, redirigir a 'home'.
    """
    if request.method == "POST":
        query = request.POST.get("query")

        if not query:
            return redirect('home')

        images = services.filterByCharacter(query)
        favourite_list = services.getAllFavourites(request)

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })

    return redirect('home')
#6ta función invoco services.py y verificar su status
def filter_by_status(request):
    """
    Filtra personajes por su estado (Alive/Deceased).
    
    Se debe implementar el filtrado de personajes según su estado.
    Se debe obtener el parámetro 'status' desde el POST, filtrar las imágenes según ese estado
    y renderizar 'home.html' con los resultados. Si no hay estado, redirigir a 'home'.
    """
    if request.method == "POST":
        status = request.POST.get("status")

        if not status:
            return redirect('home')

        images = services.filterByStatus(status)
        favourite_list = services.getAllFavourites(request)

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })

    return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    """
    favourite_list = services.getAllFavourites(request)

    #return render(request, 'home.html', {
    #    'images': services.getAllImages(),
    #    'favourite_list': favourite_list
    
    ##actualizo el redireccionamiento a "FAVOURITES"   
    return render(request, 'favourites.html', {
        'images': services.getAllImages(),
        'favourite_list': favourite_list
    })

@login_required
def saveFavourite(request):
    """
    Guarda un personaje como favorito.
    """
    if request.method == "POST":
        services.saveFavourite(request)

    return redirect('home')
    pass

@login_required
def deleteFavourite(request):
    """
    Elimina un favorito del usuario.
    """
    if request.method == "POST":
        services.deleteFavourite(request)

    return redirect('home')
    # Sin esto no podemos borrar favoritos.

@login_required
def exit(request):
    logout(request)
    return redirect('home')