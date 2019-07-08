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
    path("download/", views.DownloadBlockchain.as_view(), name="download"),
    path("getInfo/", views.getInfo, name="getInfo"),
    path("showInfo/", views.showInfo, name="showInfo"),
    path("main", views.main, name="main")
]

