import secrets
import logging

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

logger = logging.getLogger(name=__name__)

class CustomAuthToken(ObtainAuthToken):
    """
    POST : Devuelve el TOKEN del usuario, si el usuario no existe, lo crea y lo agrega al GRUPO solicitante
    """

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def post(self, request, *args, **kwargs):

        # OBTIENE EL USERNAME Y FIRST_NAME ENVIADO EN LA REQUEST
        username = request.POST.get("username", False)
        first_name = request.POST.get("first_name", False)

        if not username:
            return JsonResponse({"username": ["Este campo es requerido."] } )
        
        if not first_name:
            return JsonResponse({"first_name": ["Este campo es requerido."] } )

        try:
            # CHEQUEA SI EL USUARIO YA EXISTE
            user = User.objects.get(username=username)

            # CHEQUEA SI EL FIRST_NAME (USERNAME REAL) FUE ACTUALIZADO, Y LO CAMBIA
            if first_name != user.first_name:
                first_name_viejo = user.first_name
                user.first_name = first_name
                user.save()
                logger.error(f"Se cambio el username {first_name_viejo} por {first_name}")

        except User.DoesNotExist:
            # SI NO EXISTE, CREA UNA PASSWORD RANDOM
            password_length = 12
            password = secrets.token_urlsafe(password_length)
            
            # CREA EL USUARIO CON LOS DATOS PASASDOS Y LA NUEVA PASSWORD
            user = User.objects.create_user(username=username, first_name=first_name, password=password)

            # AÑADE EL USUARIO AL GRUPO DE SOLICITANTES
            group = Group.objects.get(id=5) 
            group.user_set.add(user)

        # DEVUELVE LA TOKEN
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})