# capa DAO de acceso/persistencia de datos.
from app.models import Favourite

def saveFavourite(fav):
    favourite, created = Favourite.objects.get_or_create(
        user=fav.user,
        name=fav.name,
        occupation=fav.occupation,
        defaults={
            'gender': fav.gender,
            'status': fav.status,
            'phrases': fav.phrases,
            'age': fav.age,
            'image': fav.image,
        }
    )
    return favourite



def getAllFavourites(user):
    """
    Obtiene todos los favoritos de un usuario desde la base de datos.
    """
    return Favourite.objects.filter(user=user)
    
#actualizo la función borrar favorito, porque no estaba validando el usuario
def deleteFavourite(favId, user):
    Favourite.objects.filter(id=favId, user=user).delete()
    return True