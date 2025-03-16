from django.contrib import admin
from django.urls import path
from map_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('map/', views.map_view, name='map_view'),
]