from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


try:
    connection = psycopg2.connect(user= "postgres.asxvaofubgqrgynnfkho",
                        password="pacilflixE14",
                        host="aws-0-ap-southeast-1.pooler.supabase.com",
                        port="6543",
                        database="postgres")

    # Create a cursor to perform database operations
    connection.autocommit = True
    cursor = connection.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [dict(row) for row in cursor.fetchall()]

def query(query_str: str):
    hasil = []
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SET SEARCH_PATH TO PUBLIC")
        try:
            cursor.execute(query_str)

            if query_str.strip().upper().startswith("SELECT"):
                # Kalau ga error, return hasil SELECT
                hasil = map_cursor(cursor)
            else:
                # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                hasil = cursor.rowcount
                connection.commit()
        except Exception as e:
            # Ga tau error apa
            hasil = e

    return hasil

# Create your views here.
def daftar_favorit_view(request):
    user = request.session["username"]
    query_str = f"SELECT * FROM daftar_favorit WHERE username = '{user}'"
    hasil = query(query_str)
    context = {
        "user" : user,
        "hasil" : hasil,
    }

    return render(request, 'daftar-favorit.html', context)

def detail_daftar_favorit(request, daftar_favorit,timestamp):
    print("halo3")
    user = request.session["username"]
    query_str = f"""SELECT t.judul, tdf.timestamp, t.id FROM tayangan_memiliki_daftar_favorit tdf, 
                    tayangan t WHERE tdf.timestamp = '{timestamp}' 
                    and tdf.username = '{user}' and t.id = tdf.id_tayangan"""
    hasil = query(query_str)
    context = {
        "hasil" : hasil,
        "nama_daftar" : daftar_favorit,
    }
    return render (request, 'detail-daftar-favorit.html', context)

"""
Masih ada yang kurang
"""
def delete_daftar_favorit_tayangan(request, daftar_favorit, tayangan, timestamp):
    print("halo1")
    user = request.session["username"]
    query_str = f"""DELETE FROM tayangan_memiliki_daftar_favorit 
                    WHERE id_tayangan = '{tayangan}' 
                    AND timestamp = '{timestamp}' AND username = '{user}';"""
    hasil=query(query_str)
    print(hasil)
    return HttpResponseRedirect(reverse('daftar_favorit:detail-daftar-favorit',kwargs={'daftar_favorit': daftar_favorit, 'timestamp':timestamp }))

def delete_daftar_favorit(request, timestamp):
    print("halo")
    user = request.session["username"]
    query_str = f"""DELETE FROM daftar_favorit 
                    WHERE timestamp = '{timestamp}' 
                    AND username ='{user}';"""
    hasil = query(query_str)
    print(hasil)
    return HttpResponseRedirect(reverse('daftar_favorit:daftar-favorit'))

    

def insert_dummy(request):
    query_str = f"""INSERT INTO daftar_favorit 
    VALUES('2024-04-21 23:07:00', 'dustybun', 
    'Daftar Favorit 17');"""
    hasil = query(query_str)
    print(hasil)
