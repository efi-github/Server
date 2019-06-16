from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

#Gibt die URL's an die vom Clienten angeschrieben werden können
urlpatterns = [
    path("", include(router.urls)),
    path("block/", views.BlockView.as_view()),
    path("block/<slug:uuid>/", views.BlockView.as_view()),
    path("pfandWebsite/", views.PfandWebsite.as_view()),
    path("registrierungWebsite/", views.RegistrierungWebsite.as_view()),
    path("anmeldung/", views.Anmeldung.as_view()),
    path("abmeldung/", views.abmeldung),
    path("download/", views.DownloadBlockchain.as_view()),
]