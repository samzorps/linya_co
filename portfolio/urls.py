from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('images/', views.image_list, name='image_list'),
    path('image_collections/', views.image_collection_list, name='image_collections'),
    path('code_projects/', views.code_project_list, name='code_projects'),
]
