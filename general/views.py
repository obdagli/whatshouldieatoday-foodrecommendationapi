from django.shortcuts import render
from .models import Food, Foodadd
from .serializers import UserSerializer, LoginSerializer,RegisterSerializer,FoodSerializer,FoodAddSerializer
from rest_framework import status,permissions, viewsets, generics, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json
from rest_framework.decorators import action
import random
from django.db.models import Count
import numpy as np
import simplejson as json
from RecSystems.contentbased import rec_cbcalculator
from RecSystems.collaborative import rec_clcalculator
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView

class UserViewSet(viewsets.ModelViewSet):
    #Kullanıcı ekleme, silme, güncelleme işlemleri için oluşturulan;
    #ModelViewSet. Django rest framework aracılığıyla bu oluşturulan ModelViewSet
    #Yukarıda bahsi geçen bütün işlemleri kendi içerisinde ypar.
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET', 'POST'])
def FoodViewSet(request):
    #Yenilen yemekleri görmek amacıyla kullanıcı "GET" isteği yolladığında
    #Gelen kullanıcının id'sine göre yenilen yemekler tablosunda filtreleme yapıp, kullanıcıya döndürür.
    if request.method == 'GET':
        udata = request.user
        query = Food.objects.filter(userfk = udata.id)
        serializer = FoodSerializer(query, many=True)
        return Response(serializer.data)

    #Yemek ekleme amacıyla "POST" isteği yollandığında
    #Gelen kullanıcının id'si ve yemek istediği yemek id'sine göre tabloya ekleme yapılır.
    elif request.method == 'POST':
        permission_classes = [
        permissions.IsAuthenticated,
    ]
    consumed = Food()
    consumed.food = Foodadd.objects.get(id=request.POST.get("yemek_id"))
    consumed.userfk = request.user
    consumed.save()
    return Response(status=status.HTTP_201_CREATED)

class FoodaddViewSet(viewsets.ModelViewSet):
    #Tüm yemeklerin bulunduğu tablo.
    #Bu tabloya admin panel aracılığıyla yemek eklenebilir/silinebilir/düzenlenebilir.
    queryset = Foodadd.objects.all()
    serializer_class = FoodAddSerializer

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user,
            context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
@api_view(['GET'])
def userfood_view(request):    

    foodser = Food.objects.all()
    serializer = FoodSerializer(foodser,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def rec_contentbased(request):
    if request.method == 'GET':
        permissions_classes = [permissions.IsAuthenticated]
    #Gelen "request"in Authorization Token'ini kontrol edip devam edip etmemesi gerektiğini kontrol eder.
    #Kontrolden sonra Token'i ile işlem yapan kullanıcının bilgilerini tutmak adına "request.user" kullanılır.
    user_data = request.user
    food = Food.objects.filter(userfk=user_data.id) #Request yapan user'ın id'sini yenilen yemekler tablosunda arar.
    #Arama sonucu 0 ise yani kullanıcı hiç yemek yememiş ise;
    #Cold-start(En fazla tüketilen 8 yiyeceği döndürür ve hiç yemek yemeyen bir kullanıcı için popüler önerileri sunar)
    #-------------------------------------------------------------------------------------------------------------------
    if not food:
        eatenfoods = Food.objects.values('food_id').annotate(Count('food_id')).order_by('-food_id__count')
        idholder = []
        popularfood = []
        for t in eatenfoods:
            idholder.append(t['food_id'])
        for y in range(8):
            popularfood.append(idholder[y])
        queryset = Foodadd.objects.filter(id__in = popularfood)
        serializer = FoodAddSerializer(queryset, many=True)
        return Response(serializer.data)
    #-------------------------------------------------------------------------------------------------------------------
    #İçerik bazlı filtreleme olduğu için bütün yemeklerin malzemeleri(ingredients) baz alınmalı,
    #Serializer aracılığıyla bütün yemekler seçilir, id'leri bir dizide tutulur.
    queryset = Foodadd.objects.all()
    columns = ['id','food_ingredients']
    q_list = list(queryset)
    temp = []
    arrangeArray(temp,q_list)#Geçici arraylere atama işlemleri bir başka fonksiyonda yapılıyor
    df = pd.DataFrame(temp, columns=columns)   
     
    rnd_foods = []
    serializer = FoodSerializer(food, many=True)
    for i in range(len(serializer.data)):
        rnd_foods.append(serializer.data[i]['food']) 

    #Kullanıcının yediği yemeklerden rastgele olarak bir yemek seçilir ve bu yemeğe benzer 5 adet yemek önermesi amacıyla,
    #"rec_cbcalculator" fonksiyonu yani ContentBased fonksiyonu çağırılır(yukarıda import edildi)
    predfoods = []
    predfoods = rec_cbcalculator(df, random.choice(rnd_foods), 5)
    queryset2 = Foodadd.objects.filter(id__in=predfoods)
    serializer = FoodAddSerializer(queryset2, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def rec_collaborative(request):    
    #Kullanıcı-Yemek matrisleri oluşturulması amacıyla kullanıcı ve yemeklerin
    #Toplam yeme sayıları bulunur ve bunlar iki ayrı arrayde tutulur collaborative
    #içerisinde birleştirilerek bir matris elde edilir.
    if request.method == 'GET':
        permissions_classes = [permissions.IsAuthenticated]
    eatenfoods = Food.objects.values(
        'userfk_id', 'food_id').annotate(Count('food_id')).order_by('userfk_id')
    temparr = []
    temparr2 = []
    users = User.objects.all()
    foods = Foodadd.objects.all()
    user_data = request.user
    
    for i in eatenfoods:
        result = i.items()
        data = list(result)
        numpyArray = np.array(data)
        temparr2.append(numpyArray)

    for i in users:
        i = []
        for x in foods:
            i.append(0)
        temparr.append(i)

    count = 0
    for i in users:
        count2 = 0
        for k in foods:
            for j in temparr2:
                if(int(j[0][1]) == i.id and int(j[1][1]) == k.id):
                    temparr[count][count2] = temparr[count][count2] + int(j[2][1])
            count2 = count2 + 1
        count = count + 1

    foodid = rec_clcalculator(temparr, users, foods, user_data)
    getfood = Foodadd.objects.filter(id = foodid+1)
    serializer = FoodAddSerializer(getfood,many=True)
    return Response(serializer.data)


def arrangeArray(temp,q):
    x = 0
    for i in q:
        temp2 = []
        temp2.append(i.id)
        temp2.append(i.food_ingredients)
        temp.append(temp2)
        x = x + 1
        temp2.remove
    return temp
class removefoodbyuser(ListModelMixin, CreateModelMixin, GenericAPIView, DestroyModelMixin):
    #Yenilen yemeğin silinme işlemi.
    #Gelen kullanıcı primary key'ine göre silme işlemi yapar.
    queryset = Food.objects.all() 
    serializer_class = FoodSerializer 
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk): 
        return self.destroy(request, pk) 
    