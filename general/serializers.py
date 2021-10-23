from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Food, Foodadd
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    #DRF(Rest Framework)içerisinde kendisine ait User tablosu bulunmaktadır.
    #Biz bu tabloyu kullanarak, kullanıcı oluşturma, güncelleme işlemlerini yapabiliriz.
    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    def update(self, instance, validated_data):
        if 'user' in validated_data:
            instance.user.password = make_password(
                validated_data.get('user').get('password', instance.user.password)
            )
            instance.user.save()
    class Meta:
        #API arayüzünde ve return responselarda gözükmesi istenen fieldlar
        model = User
        fields = ['id','username','email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
        extra_kwargs = {'password':{'write_only':True}}
    #User tablosunda bir register işlemi olduğunda verilen parolanın filtrelenmesi gerekmektedir dolayısıyla
    #Bu işlemler bu kısımda yapılır. Knox Authorization kullanılarak REGISTER, LOGIN gibi işlemler yapıldı.
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    #ID, PW doğrulama yer. Eğer yanlışsa hata verir.
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
class FoodAddSerializer(serializers.ModelSerializer):
    #API arayüzünde ve return responselarda gözükmesi istenen fieldlar
    class Meta:
        model = Foodadd
        fields = 'id', 'food_name','mutfak_tur','food_photolink','food_ingredients'

class FoodSerializer(serializers.ModelSerializer):
    #API arayüzünde ve return responselarda gözükmesi istenen fieldlar
    class Meta:
        model = Food
        fields = ('id', 'food','foodname','userfk','username','date','food_photolink')
    username = serializers.SerializerMethodField('get_username')
    foodname = serializers.SerializerMethodField('get_food_name')
    food_photolink = serializers.SerializerMethodField('get_food_photolink')
    def get_food_name(self,obj):
        return obj.food.food_name
    def get_username(self, obj):
        return obj.userfk.username
    def get_food_photolink(self,obj):
        return obj.food.food_photolink