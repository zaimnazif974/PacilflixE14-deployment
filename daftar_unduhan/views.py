
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
    print("halo")
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
def daftar_unduhan_view(request):
    user = request.session["username"]
    query_str = f"""SELECT t.id, t.judul, tt.username, tt.timestamp 
                FROM tayangan_terunduh tt, tayangan t 
                WHERE username = '{user}' and tt.id_tayangan = t.id"""
    hasil = query(query_str)
    context = {
        "user" : user,
        "hasil" : hasil,
    }

    return render(request, 'daftar-unduhan.html', context)

def delete_unduhan(request, timestamp,id):
    user = request.session["username"]
    # add_func=f"""DROP TRIGGER IF EXISTS before_delete_tayangan_terunduh ON tayangan_terunduh;"""
    add_func = f""" CREATE OR REPLACE FUNCTION check_delete_age()
                    RETURNS TRIGGER AS
                    $$
                    BEGIN
                        IF (SELECT NOW() - OLD.timestamp < INTERVAL '1 day')
                        THEN RAISE EXCEPTION 'Tayangan belum memiliki masa 
                        unduh 1 hari';
                        END IF;
                    RETURN OLD;
                    END;
                    $$
                    LANGUAGE plpgsql;"""
    hasil_func = query(add_func)
    # add_trigger = f""" DROP FUNCTION IF EXIST check_delete_age();"""
    add_trigger = f"""CREATE OR REPLACE TRIGGER before_delete_tayangan_terunduh
                    BEFORE DELETE ON tayangan_terunduh
                    FOR EACH ROW
                    EXECUTE FUNCTION check_delete_age();"""
    hasil_trig= query(add_trigger)
    query_str = f"""
                    DELETE FROM tayangan_terunduh 
                    WHERE timestamp = '{timestamp}' 
                    AND username ='{user}' AND id_tayangan = '{id}';"""

    
    hasil = query(query_str)
    if hasil == 1:
        return HttpResponseRedirect(reverse('daftar_unduhan:daftar-unduhan'))
    messages.error(request, "Tayangan terunduh kurang dari 1 hari tidak dapat dihapus!!")
    return HttpResponseRedirect(reverse('daftar_unduhan:daftar-unduhan'))

def insert_dummy(request):
    query_str = f"""INSERT INTO tayangan_terunduh 
                VALUES ( 'fcc26335-ad7f-43e3-a3d6-9231fe7df9b3', 'dustybun', '2024-05-17 17:24:54');"""
    hasil = query(query_str)
    print(hasil)