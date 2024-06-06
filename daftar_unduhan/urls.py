from django.urls import path
from . import views
from .views import daftar_unduhan_view,insert_dummy,delete_unduhan

app_name = 'daftar_unduhan'

urlpatterns = [
    path('', daftar_unduhan_view, name='daftar-unduhan'),
    path('insert-dummy', insert_dummy, name='insert-dummy'),
    path('delete/<uuid:id>/<timestamp:timestamp>', delete_unduhan, name='delete-unduhan')
]

