from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id} - {self.name}'

    
class Model(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Car(models.Model):
    name = models.CharField(max_length=500)
    year = models.BigIntegerField()
    size = models.FloatField()
    milage = models.FloatField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="my_car", blank=True, null=True)

    def __str__(self):
        return self.name



def photos_dir(instanse, filename):
    usrnme = f'{instanse.car.name}'
    folder_name = f"{usrnme}/{filename}"
    return folder_name
class Image(models.Model):
    image = models.ImageField(upload_to=photos_dir)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_img")


