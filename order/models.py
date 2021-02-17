from django.db import models


class Order(models.Model):
    car = models.ForeignKey("cars.Car", on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    service = models.ForeignKey("service.Service", on_delete=models.CASCADE, blank=True, null=True)
    subservice = models.ForeignKey("service.SubService", on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    is_finished = models.BooleanField(default=False)
    in_work = models.BooleanField(default=False)

    price = models.BigIntegerField(blank=True, null=True)
    cto = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True, related_name="order_cto")

    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} {self.car.name}'



def photos_dir(instanse, filename):
    usrnme = f'{instanse.order.car.name}'
    folder_name = f"{usrnme}/{filename}"
    return folder_name
class Image(models.Model):
    image = models.ImageField(upload_to=photos_dir)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_img")

    def __str__(self):
        return f'{self.id} {self.order.car.name}'


class OrderRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.BigIntegerField()
    time = models.CharField(max_length=150,blank=True, null=True)
    cto = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.id} {self.price}'