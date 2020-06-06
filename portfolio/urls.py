from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('art/pieces/store', views.store, name='store_list_view'),
    path('art/pieces/<str:name>/', views.ArtPieceDetailView.as_view(), name='art_piece_detail'),
    path('art/collections/<str:name>/', views.ArtCollectionDetailView.as_view(), name='art_collection_detail'),
    path('code/<str:name>/', views.CodeProjectDetailView.as_view(), name='code_project_detail'),
    path('art/pieces/', views.ArtPieceListView.as_view(), name='art_piece_list'),
    path('art/collections/', views.ArtCollectionListView.as_view(), name='art_collection_list'),
    path('code/', views.CodeProjectListView.as_view(), name='code_project_list'),
]
