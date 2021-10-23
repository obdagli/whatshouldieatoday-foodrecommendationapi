from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
# Create your models here.
class Foodadd(models.Model):
    food_name = models.CharField(max_length=150)
    food_photolink = models.CharField(max_length=200, default="link will be here")
    food_photo = models.ImageField(null=True, blank=True, upload_to='foodPhotos/%Y/%m/')
    food_ingredients = models.TextField(blank=True, null=True)
    AFRIKA = 'Afrika'
    ASYA = 'Asya'
    AVRUPA = 'Avrupa'
    ORTADOGU = 'Orta Doğu'
    KUZEYAMERIKA = 'Kuzey Amerika'
    GUNEYAMERIKA = 'Güney Amerika'
    OKYANUSYA = 'Okyanusya'
    DIGER = 'Diğer'
    mutfak_choice = [
        (AFRIKA, 'Afrika'),
        (ASYA, 'Asya'),
        (AVRUPA, 'Avrupa'),
        (ORTADOGU, 'Orta Doğu'),
        (KUZEYAMERIKA, 'Kuzey Amerika'),
        (GUNEYAMERIKA, 'Güney Amerika'),
        (OKYANUSYA, 'Okyanusya'),
        (DIGER, 'Diğer'),
    ]
    mutfak_tur = models.CharField(max_length=20,choices=mutfak_choice,default=DIGER)

    def save(self, *args, **kwargs):
        # IMAGE RESIZE
        super().save(*args, **kwargs)
        if self.food_photo:
            img = Image.open(self.food_photo.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.food_photo(output_size)
                img.save(self.food_photo.path)
    def __str__(self):
        return self.food_name
class Food(models.Model):
    
    food = models.ForeignKey(Foodadd, on_delete=models.CASCADE)
    userfk = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="User ID")
    date = models.DateField(auto_now=True)