from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Recherche
    path('search/', views.video_search, name='video_search'),
    
    # Catégories
    path('category/<slug:slug>/', views.video_category, name='video_category'),
    
    # Upload
    path('upload/', views.video_upload, name='video_upload'),
    
    # Détail, modification, suppression, like, téléchargement
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('video/<int:video_id>/download/', views.video_download, name='video_download'),
    path('video/<int:video_id>/edit/', views.video_edit, name='video_edit'),
    path('video/<int:video_id>/delete/', views.video_delete, name='video_delete'),
    path('video/<int:video_id>/like/', views.video_like, name='video_like'),
    path('video/<int:video_id>/stream/', views.video_stream, name='video_stream'),
]

