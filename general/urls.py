from django.urls import path
from django.conf.urls import url, include
from general import views
from knox import views as knox_views
from rest_framework.routers import DefaultRouter
#from views import removefoodbyuser
router = DefaultRouter()
router.register(r'foodadd', views.FoodaddViewSet)   #Yeni yemek oluşturma url'i
router.register(r'users', views.UserViewSet)    #User listesi.
urlpatterns = [
    url(r'^', include(router.urls)),
    path('food_consumedlist/', views.userfood_view),    #Tüm kullanıcılara ait yenilen yemek listesi
    path('food_consumeduser/', views.FoodViewSet),      #İsteği yollayan kullanıcıya ait yenilen yemek listesi
    path('removefoodbyuser/<int:pk>', views.removefoodbyuser.as_view(), name='removefoodbyuser'), #<int:pk> yazan yere, kullanıcı silmek istediği column'un id'sini yollar.
    path('rec_contentbased/', views.rec_contentbased),  #Kullanıcı Authorization Token kullanarak kendine ait "content based" önerisi alır.
    path('rec_collaborative/', views.rec_collaborative),    #Kullanıcı Authorization Token kullanarak kendine ait "collaborative" önerisi alır.
    path('register/',views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout')
]