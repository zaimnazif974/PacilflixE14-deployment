from django.urls import path
from .views import kelola_langganan_view, beli_paket_view, add_transaction

urlpatterns = [
    path('', kelola_langganan_view, name='kelola_langganan'),
    path('beli-paket/<str:package_name>/', beli_paket_view, name='beli_paket'),
    path('add-transaction/<str:package_name>/', add_transaction, name='add_transaction'),
]
