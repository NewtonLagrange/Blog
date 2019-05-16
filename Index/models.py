from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return self.name
