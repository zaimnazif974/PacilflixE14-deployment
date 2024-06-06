from django.urls import path
import tayangan.views as views

app_name = 'tayangan'

urlpatterns = [
    path('trailer-tayangan/', views.show_trailer, name='show_trailer'),
    path('daftar-tayangan/', views.show_tayangan, name='show_tayangan'),
    path('search/', views.show_search, name='show_search'),
    path('film/<str:id>', views.show_film, name='show_film'),
    path('series/<str:id>', views.show_series, name='show_series'),
    path('episode/<str:id>', views.show_episode, name='show_episode'),
    path('unduh/<str:id>', views.add_unduh, name='add-unduhan'),
    path('add-to-favorit/<uuid:id>', views.add_to_favorit, name='add-to-favorit' ),

    path('api/tayangan/popular', views.get_popular_tayangan, name='get_popular_tayangan'),
    path('api/tayangan/search', views.search_tayangan, name='search_tayangan'),
    path('api/film', views.get_all_films, name='get_all_films'),
    path('api/series', views.get_all_series, name='get_all_series'),
    path('api/film/<str:id>', views.get_film_detail, name='get_film_detail'),
    path('api/series/<str:id>', views.get_series_detail, name='get_series_detail'),
    path('api/series/<str:id_series>/episode/<str:subjudul>', views.get_series_episode, name='get_series_episode'),
    path('api/tayangan/tonton', views.tonton_tayangan, name='tonton_tayangan'),
    
    path('api/ulasan', views.create_ulasan, name='create_ulasan'),
    path('api/ulasan/<str:tayangan_id>', views.get_ulasan, name='get_ulasan'),
]
