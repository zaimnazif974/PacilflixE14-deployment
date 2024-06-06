from django.db import connection
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT a.username,a.password 
                           FROM public.pengguna as a 
                           WHERE a.username = %s AND a.password = %s
                           """, [username, password])
            user = cursor.fetchone()

        if user is not None:
            username_str = str(user[0])
            request.session['username'] = username
            request.session['is_authenticated'] = True
            return redirect('/daftar-tayangan/')
        else:
            messages.error(request, 'Sorry, incorrect username or password. Please try again.')
    return render(request, 'login.html')


# users = [
#     {"username": "hermionegranger", "password": "Hg#123456", "id_tayangan": "ef6f8cdf-4f64-4e0d-9412-6b1ac7b2b3dc", "negara_asal": "Prancis"},
#     {"username": "jennierubyjane", "password": "Jrj#123456", "id_tayangan": "2061ff63-5993-49d8-a574-4b42bf850f57", "negara_asal": "Korea Selatan"},
#     # add pengguna
# ]

# def find_user(username):
#     for user in users:
#         if user['username'] == username:
#             return user
#     return None

from django.db import IntegrityError


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara_asal = request.POST.get('country')

        try:
            with connection.cursor() as cursor:
                # Insert new user
                cursor.execute("""
                               INSERT INTO public.pengguna (username, password, negara_asal)
                               VALUES (%s, %s, %s)
                               """, [username, password, negara_asal])
            # Redirect to login page after successful registration
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('/auth/login/')

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'register.html')



def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('/auth/login/')  
