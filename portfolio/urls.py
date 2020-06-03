from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
#    path('art/pieces/store', views.StoreView, name='store_list_view'),
    path('art/pieces/<str:name>/', views.ArtPiecetDetailView.as_view(), name='art_piece_detail'),
#    path('art/collections/<string:name>/', views.ArtCollectionDetailView.as_view(), name='art_collection_detail'),
#    path('art/pieces/', views.ArtPiecetListView.as_view(), name='art_piece_list'),
    path('art/collections/', views.CollectionListView.as_view(), name='art_collection_list'),
    path('code/', views.CodeProjectListView.as_view(), name='code_project_list'),
]
