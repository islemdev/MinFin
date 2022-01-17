from django.urls import path
from . import views

urlpatterns = [
    path('show/<cin>/', views.show),
    path('insertCitoyen', views.insertCitoyen),
    path('insertInfraction', views.insertInfraction),

]





