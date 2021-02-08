from django.db import models


def photos_dir(instanse, filename):
    usrnme = f'{instanse.name}'
    folder_name = f"{usrnme}/{filename}"
    return folder_name

class CTO(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to=photos_dir)
    cto_id = models.CharField(max_length=50)


    def __str__(self):
        return self.name