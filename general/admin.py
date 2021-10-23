from django.contrib import admin
from .models import Food,Foodadd
# Register your models here.,
@admin.register(Foodadd)
class FoodaddModel(admin.ModelAdmin):
    list_display = ('food_name', 'mutfak_tur')
@admin.register(Food)
class FoodsModel(admin.ModelAdmin):
    list_display = ('food', 'userfk')