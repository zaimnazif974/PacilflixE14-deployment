from django.urls import path
from . import views
import datetime
from django.urls import register_converter
from .views import daftar_favorit_view, detail_daftar_favorit, insert_dummy, delete_daftar_favorit_tayangan
from .views import delete_daftar_favorit
app_name = 'daftar_favorit'

'''
to_python : convert string into datetime
to_url : convert datetime into string
'''
class TimestampConverter:
    regex = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'  # YYYY-MM-DD HH:mm:ss

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    def to_url(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')

register_converter(TimestampConverter, 'timestamp')

urlpatterns = [
    path('', daftar_favorit_view, name='daftar-favorit'),
    path('detail/<str:daftar_favorit>/<timestamp:timestamp>', detail_daftar_favorit, name='detail-daftar-favorit'),
    path('insert-dummy', insert_dummy, name='insert-dummy'),
    path('delete/<str:daftar_favorit>/<uuid:tayangan>/<timestamp:timestamp>', delete_daftar_favorit_tayangan, name='delete-tayangan-daftar-favorit'),
    path('<timestamp:timestamp>', delete_daftar_favorit, name='delete-daftar-favorit'),
]

