from django.contrib import admin
from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',views.signupView, name='signup'),
    path('verify/',views.verify, name='verify'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgotpasswordEmail/',views.forgotpasswordEmail, name='forgotpasswordEmail'),
    path('setPassword/',views.setPassword, name='setPassword'),
    path('homeSlider/',views.homeSlider, name='homeSlider'),
    path('homeBlock/',views.homeBlock, name='homeBlock'),
    path('products/',views.products, name='products'),
    path('newArrivals/',views.newArrivals, name='newArrivals'),
    path('offers/',views.offers, name='offers'),
    path('collections/',views.collections, name='collections'),
    path('search/',views.search, name='search'),
]
