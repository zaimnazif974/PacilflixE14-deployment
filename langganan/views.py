from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

@login_required
def kelola_langganan_view(request):
    username = request.user.username  # Use the logged-in user's username
    active_subscription = get_active_subscription(username)
    transaction_history = get_transaction_history(username)
    recommended_packages = get_packages()

    context = {
        'active_subscription': active_subscription,
        'transaction_history': transaction_history,
        'recommended_packages': recommended_packages,
    }

    return render(request, 'kelola_langganan.html', context)

@login_required
def beli_paket_view(request, package_name):
    package_info = get_package_info(package_name)

    context = {
        'package_info': package_info,
        'package_name': package_name,
    }

    return render(request, "beli_paket.html", context)

@login_required
def add_transaction(request, package_name):
    if request.method == 'POST':
        username = request.user.username
        payment_method = request.POST.get('metode_pembayaran')

        # Check if user already has an active subscription
        active_subscription = get_active_subscription(username)
        if active_subscription:
            # Update existing subscription
            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO public")
                cursor.execute("""
                    UPDATE TRANSACTION
                    SET end_date_time = %s, nama_paket = %s, metode_pembayaran = %s, timestamp_pembayaran = CURRENT_TIMESTAMP
                    WHERE username = %s AND end_date_time >= %s
                """, (datetime.now().date() + timedelta(days=30), package_name, payment_method, username, datetime.now()))
        else:
            # Insert new subscription
            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO public")
                cursor.execute("""
                    INSERT INTO TRANSACTION (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """, (username, datetime.now().date(), datetime.now().date() + timedelta(days=30), package_name, payment_method))

        return redirect('main:kelola_langganan')
    else:
        return redirect('main:kelola_langganan')

def get_users():
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")
        cursor.execute("SELECT username FROM PENGGUNA")
        users = cursor.fetchall()
    return [user[0] for user in users]

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
