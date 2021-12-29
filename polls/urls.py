from django.urls import path
from . import views

urlpatterns = [
path('show/<cin>/',views.show),
]





