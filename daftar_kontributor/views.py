from django.shortcuts import render
from django.db import connection
# import logging # debug

# logger = logging.getLogger(__name__) # debug

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
