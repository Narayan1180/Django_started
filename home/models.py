from django.db import models

# Create your models here.

# myapp/models.py


class FormData(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.surname}"

