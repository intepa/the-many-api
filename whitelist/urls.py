from django.urls import path
from . import views

urlpatterns = [
    path('whitelist/<str:address>', views.whitelistAddress,
         name="whitelist-address"),
]
