from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_kontributor_view, name='daftar_kontributor'),
]
