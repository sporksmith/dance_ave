from django.db import models

class SongStation(models.Model):
    audio_url = models.URLField()
    select_code = models.CharField(max_length=10, db_index=True)
    complete_code = models.CharField(max_length=10, db_index=True)

# Create your models here.
class Player(models.Model):
    address = models.CharField(max_length=100, db_index=True)
    completed_stations = models.ManyToManyField(SongStation)

