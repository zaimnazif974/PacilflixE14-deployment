from django.db import models

class Sutradara(models.Model):
    id = models.UUIDField(primary_key=True)
    nama = models.CharField(max_length=50)
    jenis_kelamin = models.IntegerField(choices=((0, 'Laki-laki'), (1, 'Perempuan')))
    kewarganegaraan = models.CharField(max_length=50)

class Pemain(models.Model):
    id = models.UUIDField(primary_key=True)
    nama = models.CharField(max_length=50)
    jenis_kelamin = models.IntegerField(choices=((0, 'Laki-laki'), (1, 'Perempuan')))
    kewarganegaraan = models.CharField(max_length=50)

class PenulisSkenario(models.Model):
    id = models.UUIDField(primary_key=True)
    nama = models.CharField(max_length=50)
    jenis_kelamin = models.IntegerField(choices=((0, 'Laki-laki'), (1, 'Perempuan')))
    kewarganegaraan = models.CharField(max_length=50)
