from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Package(models.Model):
    nama = models.CharField(max_length=50, primary_key=True)
    harga = models.PositiveIntegerField()
    resolusi_layar = models.CharField(max_length=50)
    dukungan_perangkat = models.CharField(max_length=50)

class Subscription(models.Model):
    pengguna = models.OneToOneField(User, on_delete=models.CASCADE)
    paket = models.ForeignKey(Package, on_delete=models.CASCADE)
    tanggal_dimulai = models.DateField(auto_now_add=True)
    tanggal_berakhir = models.DateField(null=True, blank=True)

class Transaction(models.Model):
    pengguna = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField(auto_now_add=True)
    end_date_time = models.DateTimeField(null=True, blank=True)
    paket = models.ForeignKey(Package, on_delete=models.CASCADE)
    metode_pembayaran = models.CharField(max_length=50)
    timestamp_pembayaran = models.DateTimeField(auto_now_add=True)
