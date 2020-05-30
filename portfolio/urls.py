from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('code', views.code_home, name='code_home'),
    path('art', views.art_home, name='art_home')
]
