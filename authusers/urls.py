from django.urls import path
from .views import connexion,register,deconnexion
app_name = "authusers"

urlpatterns = [
    path('connexion',connexion,name="connexion"),
    path('register',register,name="register"),
    path('deconnexion',deconnexion,name="deconnexion")
]