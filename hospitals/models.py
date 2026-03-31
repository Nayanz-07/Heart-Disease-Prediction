from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    beds = models.IntegerField(default=0)
    rating = models.FloatField(default=4.0)

    def __str__(self):
        return f"{self.name} – {self.city}"
