from django.db import models

# Create your models here.


class Drug(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    drug_image = models.ImageField(null=True, blank=True, upload_to="media/drugImg")
    form = models.CharField(max_length=100)
    ingredient = models.TextField(max_length=200)

    def __str__(self):
        return self.name
