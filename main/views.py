from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import IntegrityError, connection, transaction
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib import messages
from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor


try:
    connection = psycopg2.connect(user= "postgres.asxvaofubgqrgynnfkho",
                        password="pacilflixE14",
                        host="aws-0-ap-southeast-1.pooler.supabase.com",
                        port="5432",
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


def show_main(request):
    return render(request, 'main.html')

def landing_view(request):
    return render(request, 'landing.html')

def daftar_kontributor_view(request):
    query = """
        SELECT c.nama, c.jenis_kelamin, c.kewarganegaraan, 'sutradara' AS tipe
        FROM CONTRIBUTORS c
        JOIN SUTRADARA s ON c.id = s.id
        UNION
        SELECT c.nama, c.jenis_kelamin, c.kewarganegaraan, 'pemain' AS tipe
        FROM CONTRIBUTORS c
        JOIN PEMAIN p ON c.id = p.id
        UNION
        SELECT c.nama, c.jenis_kelamin, c.kewarganegaraan, 'penulis' AS tipe
        FROM CONTRIBUTORS c
        JOIN PENULIS_SKENARIO ps ON c.id = ps.id;
    """
    
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute(query)
        contributors = cursor.fetchall()

    selected_filter = request.GET.get('tipe', 'semua')

    context = {
        'contributors': contributors,
        'selected_filter': selected_filter,
    }
    return render(request, 'daftar_kontributor.html', context)

def kelola_langganan_view(request):
    username = request.session["username"]
    active_subscription = get_active_subscription(username)
    transaction_history = get_transaction_history(username)
    recommended_packages = get_packages()

    # print(recommended_packages) # debug
    # print(username) # debug

    context = {
        'active_subscription': active_subscription,
        'transaction_history': transaction_history,
        'recommended_packages': recommended_packages,
    }

    return render(request, 'kelola_langganan.html', context)

def beli_paket_view(request, package_name):
    package_info = get_package_info(package_name)

    context = {
        'package_info': package_info,
        'package_name': package_name,
    }

    # print(package_info) # debug

    return render(request, "beli_paket.html", context)

def get_active_subscription(username):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("""
            SELECT 
                P.nama AS nama_paket,
                P.harga,
                P.resolusi_layar,
                D.dukungan_perangkat,
                T.start_date_time,
                T.end_date_time
            FROM 
                TRANSACTION T
            JOIN 
                PAKET P ON T.nama_paket = P.nama
            JOIN 
                DUKUNGAN_PERANGKAT D ON P.nama = D.nama_paket
            WHERE 
                T.username = %s
                AND %s BETWEEN T.start_date_time AND T.end_date_time
        """, [username, datetime.now()])
        active_subscription = cursor.fetchone()
        return active_subscription

def get_transaction_history(username):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("""
            SELECT 
                T.nama_paket,
                T.start_date_time,
                T.end_date_time,
                T.metode_pembayaran,
                T.timestamp_pembayaran,
                P.harga AS total_pembayaran
            FROM 
                TRANSACTION T
            JOIN 
                PAKET P ON T.nama_paket = P.nama
            WHERE 
                T.username = %s
            ORDER BY 
                T.timestamp_pembayaran DESC
        """, [username])
        transaction_history = cursor.fetchall()
        return transaction_history
    
def get_package_info(package_name):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("""
            SELECT p.nama, p.harga, p.resolusi_layar, string_agg(d.dukungan_perangkat, ', ') as dukungan_perangkat
            FROM PAKET p
            LEFT JOIN DUKUNGAN_PERANGKAT d ON p.nama = d.nama_paket
            WHERE p.nama = %s
            GROUP BY p.nama
        """, (package_name,))
        package_info = cursor.fetchone()
        return package_info
    
def get_packages():
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("""
            SELECT p.nama, p.harga, p.resolusi_layar, string_agg(d.dukungan_perangkat, ', ') as dukungan_perangkat
            FROM PAKET p
            LEFT JOIN DUKUNGAN_PERANGKAT d ON p.nama = d.nama_paket
            GROUP BY p.nama
        """)
        packages = cursor.fetchall()
        return packages
    
def add_transaction(request, package_name):
    if request.method == 'POST':
        username = request.session.get("username")
        payment_method = request.POST.get('metode_pembayaran')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO public")
                cursor.execute("""
                    INSERT INTO TRANSACTION (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
                    VALUES (%s, CURRENT_DATE, CURRENT_DATE + INTERVAL '30 days', %s, %s, CURRENT_TIMESTAMP)
                """, (username, package_name, payment_method))
            messages.success(request, "Transaksi berhasil.")
        except Exception as e:
            messages.error(request, f"Kamu sudah membeli paket hari ini")
        
        return redirect('main:kelola_langganan')
    else:
        return redirect('main:kelola_langganan')
    