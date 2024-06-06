import tayangan.queries as queries
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from datetime import datetime, timedelta
import json
from django.views.decorators.csrf import csrf_exempt
import psycopg2
from psycopg2.extras import RealDictCursor
from collections import namedtuple
from psycopg2 import Error
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.timezone import make_aware
from dateutil import parser
from django.db import connection
from tayangan.database_manager import dict_fetchall, dict_fetchone


# Create your views here.
try:
    connection_psycopg = psycopg2.connect(user= "postgres.asxvaofubgqrgynnfkho",
                        password="pacilflixE14",
                        host="aws-0-ap-southeast-1.pooler.supabase.com",
                        port="6543",
                        database="postgres")

    # Create a cursor to perform database operations
    connection_psycopg.autocommit = True
    cursor = connection_psycopg.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [dict(row) for row in cursor.fetchall()]

def query(query_str: str):
    hasil = []
    with connection_psycopg.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SET SEARCH_PATH TO PUBLIC")
        try:
            cursor.execute(query_str)

            if query_str.strip().upper().startswith("SELECT"):
                # Kalau ga error, return hasil SELECT
                hasil = map_cursor(cursor)
            else:
                # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                hasil = cursor.rowcount
                connection_psycopg.commit()
        except Exception as e:
            # Ga tau error apa
            hasil = e

    return hasil


# @csrf_exempt
# def your_view_function(request):
#     if request.method == 'POST':
#         selected_value = request.POST.get('selected')
#         # Perform your operations here
#         user = request.session["username"]
#         query_str = f"""INSERT INTO daftar_favorit VALUES('', '{user}', )"""
#         if success:
#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'An error occurred'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def add_unduh(request,id):
    dot_index = id.find('.')
    id_convert = id[:dot_index]
    user = request.session["username"]
    datetime_now = datetime.now()
    timestamp = datetime_now.timestamp()
    timestamp_object = datetime.fromtimestamp(timestamp)
    formatted_timestamp = timestamp_object.strftime("%Y-%m-%d %H:%M:%S")
    query_str = f"""INSERT INTO tayangan_terunduh VALUES 
        ( '{id}', '{user}', '{formatted_timestamp}');"""
    hasil = query(query_str)

    return JsonResponse({'status': 'success'})

def add_to_favorit(request,id):
    user=request.session["username"]
    if request.method == 'POST':
        selected_value = request.POST.get('pilihan_daftar_favorit')
        
        if selected_value:
            date_obj = parser.parse(selected_value)
            formatted_timestamp = date_obj.strftime("%Y-%m-%d %H:%M:%S")
           
            query_str = f"""INSERT INTO tayangan_memiliki_daftar_favorit 
            VALUES ('{id}', '{formatted_timestamp}', '{user}');"""
            hasil = query(query_str)
     
            return JsonResponse({'status': 'success'})
        

@require_GET
def show_trailer(request):
    return render(request, 'daftar_trailer.html')


@require_GET
def show_tayangan(request):
    return render(request, 'daftar_tayangan.html')


@require_GET
def show_search(request):
    return render(request, 'search_tayangan.html')


@require_GET
def show_film(request, id):
    user = request.session["username"]
    query_str = f"SELECT * FROM daftar_favorit WHERE username = '{user}'"
    hasil = query(query_str)
    
    query_str2 = f"SELECT * FROM daftar_unduhan WHERE usernam  = '{user}'"
    hasil2 = query(query_str2)
    
    dot_index = id.find('.')
    id_convert = id[:dot_index]
    
    context = {
        "user" : user,
        "hasil" : hasil,
        "unduhan": hasil2,
        "id_tayangan" : id_convert,
    }
    return render(request, 'film.html', context)


@require_GET
def show_series(request, id):
    user = request.session["username"]
    query_str = f"SELECT * FROM daftar_favorit WHERE username = '{user}'"
    hasil = query(query_str)
    
    dot_index = id.find('.')
    id_convert = id[:dot_index]
    
    context = {
        "user" : user,
        "hasil" : hasil,
        "id_tayangan" : id_convert,
    }
    return render(request, 'series.html', context)


@require_GET
def show_episode(request, id):
    return render(request, 'episode.html')


# Backend API

@require_GET
def get_popular_tayangan(request):
    try:
        cursor = connection.cursor()
        cursor.execute(queries.GET_POPULAR_TAYANGAN)
        tayangan = []
        for (i, row) in enumerate(dict_fetchall(cursor)):
            row = dict(row)
            row['peringkat'] = i + 1
            tayangan.append(row)
        cursor.close()
        return JsonResponse(tayangan, safe=False)
    except Exception as e:
        connection.rollback()
        return JsonResponse({'message': str(e)})


@require_GET
def get_all_films(request):
    try:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM TAYANGAN WHERE id IN (SELECT id_tayangan FROM FILM);')
        films = dict_fetchall(cursor)
        cursor.close()
        return JsonResponse(films, safe=False)
    except Exception as e:
        connection.rollback()
        return JsonResponse({'message': str(e)})


@require_GET
def get_all_series(request):
    try:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM TAYANGAN WHERE id IN (SELECT id_tayangan FROM SERIES);')
        series = dict_fetchall(cursor)
        cursor.close()
        return JsonResponse(series, safe=False)
    except Exception as e:
        connection.rollback()
        return JsonResponse({'message': str(e)})


@require_GET
def search_tayangan(request):
    try:
        cursor = connection.cursor()
        keyword = request.GET.get('keyword', '')
        cursor.execute(queries.GET_SEARCH_TAYANGAN, {
                       'keyword': f'%{keyword}%', })
        tayangan = dict_fetchall(cursor)
        cursor.close()
        return JsonResponse(tayangan, safe=False)
    except Exception as e:
        connection.rollback()
        return JsonResponse({'message': str(e)})


@require_GET
def get_film_detail(request, id):
    try:
        cursor = connection.cursor()
        cursor.execute(queries.GET_FILM_DETAIL, (id,))
        film = dict_fetchone(cursor)
        cursor.execute(queries.GET_SUTRADARA_BY_ID,
                       (film.pop('id_sutradara'),))
        film['sutradara'] = dict_fetchone(cursor)
        cursor.execute(queries.GET_GENRE_BY_TAYANGAN_ID, (id,))
        film['genres'] = dict_fetchall(cursor)
        cursor.execute(queries.GET_PEMAIN_BY_TAYANGAN_ID, (id,))
        film['pemain'] = dict_fetchall(cursor)
        cursor.execute(queries.GET_PENULIS_SKENARIO_BY_TAYANGAN_ID, (id,))
        film['penulis_skenario'] = dict_fetchall(cursor)
        cursor.close()
        return JsonResponse(film, safe=False)
    except Exception as e:
        connection.rollback()
        return JsonResponse({'message': str(e)})


@require_GET
def get_series_detail(request, id):
    try:
        cursor = connection.cursor()
        cursor.execute(queries.GET_SERIES_DETAIL, (id,))
        series = dict_fetchone(cursor)
        cursor.execute(queries.GET_EPISODE_BY_SERIES_ID, (id,))
        series['episodes'] = dict_fetchall(cursor)
        cursor.execute(queries.GET_SUTRADARA_BY_ID,
                       (series.pop('id_sutradara'),))
        series['sutradara'] = dict_fetchone(cursor)
        cursor.execute(queries.GET_GENRE_BY_TAYANGAN_ID, (id,))
        series['genres'] = dict_fetchall(cursor)
        cursor.execute(queries.GET_PEMAIN_BY_TAYANGAN_ID, (id,))
        series['pemain'] = dict_fetchall(cursor)
        cursor.execute(queries.GET_PENULIS_SKENARIO_BY_TAYANGAN_ID, (id,))
        series['penulis_skenario'] = dict_fetchall(cursor)
        cursor.close()
        return JsonResponse(series, safe=False)
    except Exception as e:
        connection.rollback()
        return JsonResponse({'message': str(e)})


@require_GET
def get_series_episode(request, id_series, subjudul):
    try:
        cursor = connection.cursor()
        subjudul = subjudul.replace('_', ' ')
        cursor.execute(queries.GET_EPISODE_BY_ID, (id_series, subjudul))
        episode = dict_fetchone(cursor)
        cursor.execute(queries.GET_OTHER_EPISODES, (id_series, subjudul))
        episode['other_episodes'] = dict_fetchall(cursor)
        cursor.close()
        return JsonResponse(episode, safe=False)
    except Exception as e:
        connection.rollback()
        return JsonResponse({'message': str(e)})


@csrf_exempt
@require_POST
def tonton_tayangan(request):
    cursor = connection.cursor()
    try:
        if 'username' not in request.session:
            return JsonResponse({'status': 'failed', 'message': 'User not authenticated'}, status=401)
        username = request.session.get('username')
        json_data = json.loads(request.body)
        id_tayangan = json_data.get('id_tayangan')
        progress_percentage = json_data.get('progress_percentage')

        cursor.execute(queries.GET_DURASI_TAYANGAN, {'id': id_tayangan})
        durasi_tayangan = dict_fetchone(cursor)['durasi']
        durasi_tonton = durasi_tayangan * progress_percentage / 100
        end_date_time = datetime.now()
        start_date_time = end_date_time - timedelta(minutes=durasi_tonton)

        cursor.execute('INSERT INTO RIWAYAT_NONTON VALUES (%s, %s, %s, %s);',
                       (id_tayangan, username, start_date_time, end_date_time))
        cursor.close()
        return JsonResponse({'status': 'success', 'message': 'Berhasil menambahkan ke riwayat tontonan.'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'message': str(e)}, status=500)


@require_GET
def get_ulasan(request, tayangan_id):
    try:
        cursor = connection.cursor()
        current_user_review = None
        if 'username' in request.session:
            username = request.session.get('username')
            cursor.execute(
                'SELECT * FROM ULASAN WHERE id_tayangan = %s AND username <> %s ORDER BY timestamp DESC;', (tayangan_id, username))
            reviews = dict_fetchall(cursor)
            cursor.execute(
                'SELECT * FROM ULASAN WHERE id_tayangan = %s AND username = %s;', (tayangan_id, username))
            current_user_review = dict_fetchone(cursor)
        else:
            cursor.execute(
                'SELECT * FROM ULASAN WHERE id_tayangan = %s ORDER BY timestamp DESC;', (tayangan_id,))
            reviews = dict_fetchall(cursor)
        cursor.close()
        return JsonResponse({'reviews': reviews, 'current_user_review': current_user_review}, safe=False)
    except Exception as e:
        connection.rollback()
        return JsonResponse({'message': str(e)})


@csrf_exempt
@require_POST
def create_ulasan(request):
    try:
        if 'username' not in request.session:
            return JsonResponse({'status': 'failed', 'message': 'User not authenticated'}, status=401)
        username = request.session.get('username')
        json_data = json.loads(request.body)
        id_tayangan = json_data['id_tayangan']
        timestamp = datetime.now()
        rating = int(json_data['rating'])
        deskripsi = json_data['deskripsi']
        cursor = connection.cursor()
        cursor.execute('INSERT INTO ULASAN VALUES (%s, %s, %s, %s, %s);',
                       (id_tayangan, username, timestamp, rating, deskripsi))
        cursor.close()
        return JsonResponse({'status': 'success', 'message': 'Ulasan berhasil ditambahkan.'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'message': str(e)})
