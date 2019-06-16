from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("block/", views.BlockView.as_view()),
    path("block/<slug:uuid>/", views.BlockView.as_view()),
    path("website/", views.Website.as_view()),
]