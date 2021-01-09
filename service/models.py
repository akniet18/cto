from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id} - {self.name}'


class SubService(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.name}'
