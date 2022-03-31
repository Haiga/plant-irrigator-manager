from django.db import models


# Create your models here.

class Specie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=180)
    water_consumption = models.FloatField()

    def __str__(self):
        return self.name

class Irrigator(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=180)
    water_flow = models.FloatField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.description

class Plant(models.Model):
    id = models.AutoField(primary_key=True)
    planting_date = models.DateField()
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    irrigator = models.ForeignKey(Irrigator, on_delete=models.CASCADE)

    def __str__(self):
        return self.specie.name + f" - {self.id}"
