from django.db import models


class SaveImagePath(models.Model):
    ID = models.AutoField(primary_key=True)
    path = models.CharField(max_length=500)
    saveDate = models.DateTimeField()
