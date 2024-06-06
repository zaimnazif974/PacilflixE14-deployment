from django.urls import path
import main.views as views
from .views import landing_view
from .views import daftar_kontributor_view
from .views import kelola_langganan_view
from .views import beli_paket_view

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('landing/', landing_view, name='landing'),
    # path('unduhan/', views.unduhan_view, name='daftar-unduhan'),
    # path('daftar-favorit/', views.daftar_favorit_view, name='daftar-favorit'),
    path('daftar-kontributor/', views.daftar_kontributor_view, name='daftar_kontributor'),
    path('langganan/', views.kelola_langganan_view, name='kelola_langganan'),
    path('beli-paket/<str:package_name>/', views.beli_paket_view, name='beli_paket'),
    path('add-transaction/<str:package_name>/', views.add_transaction, name='add_transaction'),
]
