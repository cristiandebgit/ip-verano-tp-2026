# capa de servicio/lógica de negocio

import random
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

##Esta es la primera función implementada, es funadamental para obtener las cards, es la base de todo
def getAllImages():
    """
    Obtiene todas las imágenes de personajes desde la API y las convierte en objetos Card.
    
    Esta función debe obtener los datos desde transport, transformarlos en Cards usando 
    translator y retornar una lista de objetos Card.
    """
    json_collection = transport.getAllImages()
    cards = []

    for character in json_collection:
        card = translator.fromRequestIntoCard(character)
        cards.append(card)

    return cards
##2da función implementada, filtro de busqueda por personaje
def filterByCharacter(name):
    """
    Filtra las cards de personajes según el nombre proporcionado.
    
    Se debe filtrar los personajes cuyo nombre contenga el parámetro recibido. Retorna una lista de Cards filtradas.
    """
    
    all_cards = getAllImages()
    filtered_cards = []

    for card in all_cards:
        if name.lower() in card.name.lower(): #comparo ambas variables con el mismo formato
            filtered_cards.append(card)

    return filtered_cards
  
# 3ra función implementada, filtro status
def filterByStatus(status_name):
    """
    Filtra las cards de personajes según su estado (Alive/Deceased).
    
    Se deben filtrar los personajes que tengan el estado igual al parámetro 'status_name'. Retorna una lista de Cards filtradas.
    """
    all_cards = getAllImages()
    filtered_cards = []

    for card in all_cards:
        if card.status.lower() == status_name.lower():
            filtered_cards.append(card)

    return filtered_cards
  

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    """
    Guarda un favorito en la base de datos.
    
    Se deben convertir los datos del request en una Card usando el translator,
    asignarle el usuario actual, y guardarla en el repositorio.
    """
    card = translator.fromTemplateIntoCard(request)
    card.user = get_user(request)

    repositories.saveFavourite(card)


def getAllFavourites(request):

    if request.user.is_authenticated:
        repo_favs = repositories.getAllFavourites(request.user)

        cards = []
        
        for fav in repo_favs:
            card = translator.fromRepositoryIntoCard({
                'id': fav.id,
                'name': fav.name,
                'gender': fav.gender,
                'status': fav.status,
                'occupation': fav.occupation,
                'phrases': fav.phrases,
                'age': fav.age,
                'image': fav.image
            })
            cards.append(card)

        return cards

    return []


def deleteFavourite(request):
    """
    Elimina un favorito de la base de datos.
    
    Se debe obtener el ID del favorito desde el POST y eliminarlo desde el repositorio.
    """
    fav_id = request.POST.get("id")
    if fav_id:
        repositories.deleteFavourite(fav_id)
  