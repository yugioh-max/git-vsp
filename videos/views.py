from django.shortcuts import render
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# Create your views here.
# ============================================
# IMPORTS
# ============================================

# Django : raccourcis pratiques
from django.shortcuts import render, redirect, get_object_or_404
# render    → afficher un template HTML avec des données
# redirect  → rediriger vers une autre page
# get_object_or_404 → chercher un objet ou afficher "Page introuvable" (404)

# Django : protection des vues
from django.contrib.auth.decorators import login_required
# @login_required → bloque l'accès si l'utilisateur n'est pas connecté

# Django : réponses spéciales
from django.http import FileResponse
# FileResponse → envoyer un fichier au navigateur (téléchargement)

# Django : messages flash
from django.contrib import messages
# messages.success/error → afficher des notifications à l'utilisateur

# Nos modèles
from .models import Video, Category
# Video  → table des vidéos
# Category → table des catégories

# Modèles des autres apps
from interactions.models import Like, Comment
# Like    → table des likes
# Comment → table des commentaires

from subscriptions.models import Subscription
# Subscription → table des abonnements

# Nos formulaires
from .forms import VideoUploadForm, VideoEditForm
# VideoUploadForm → formulaire pour publier une vidéo
# VideoEditForm   → formulaire pour modifier une vidéo


# ============================================
# VUES
# ============================================

def home(request):
    """
    Page d'accueil
    Affiche toutes les vidéos publiques, des plus récentes aux plus anciennes
    """
    videos = Video.objects.filter(visibility='public').order_by('-created_at')
    categories = Category.objects.all()
    
    return render(request, 'home.html', {
        'videos': videos,
        'categories': categories,
    })


def video_detail(request, video_id):
    """
    Page de détail d'une vidéo
    Affiche le lecteur, les infos, les commentaires, les boutons d'action
    """
    # Trouver la vidéo (ou erreur 404 si elle n'existe pas)
    video = get_object_or_404(Video, id=video_id)
    
    # Augmenter le compteur de vues
    video.views_count += 1
    video.save()
    
    # Par défaut, l'utilisateur n'a pas liké et n'est pas abonné
    liked = False
    subscribed = False
    
    # Si l'utilisateur est connecté, vérifier son like et son abonnement
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, video=video).exists()
        subscribed = Subscription.objects.filter(
            subscriber=request.user,
            creator=video.creator
        ).exists()
    
    #Gestion du commentaire
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                user=request.user,
                video=video,
                content=content
            )
            messages.success(request, "Commentaire ajouté !")
            return redirect ('video_detail', video_id=video.id)
        else:
            messages.error(request, "Le commentaire ne peut pas être vide")

    comments = video.comments.filter(parent=None)
    
    return render(request, 'video_detail.html', {
        'video': video,
        'comments': comments,
        'liked': liked,
        'subscribed': subscribed,
    })


def video_download(request, video_id):
    """
    Télécharger une vidéo sur son appareil
    Force le navigateur à télécharger le fichier au lieu de le lire
    """
    video = get_object_or_404(Video, id=video_id)
    
    # Ouvrir le fichier vidéo
    response = FileResponse(video.video_file.open(), as_attachment=True)
    
    # Dire au navigateur : "Télécharge ce fichier sous le nom titre.mp4"
    response['Content-Disposition'] = f'attachment; filename="{video.title}.mp4"'
    
    return response


@login_required
def video_upload(request):
    """
    Publier une nouvelle vidéo
    Accessible uniquement aux utilisateurs connectés (@login_required)
    """
    if request.method == 'POST':
        # L'utilisateur a envoyé le formulaire
        form = VideoUploadForm(request.POST, request.FILES)
        # request.POST  → données textuelles (titre, description...)
        # request.FILES → fichiers uploadés (vidéo, miniature)
        
        if form.is_valid():
            # Le formulaire est valide → on crée la vidéo
            video = form.save(commit=False)  # commit=False = ne pas sauvegarder tout de suite
            video.creator = request.user      # Ajouter le créateur (l'utilisateur connecté)
            video.save()                      # Maintenant on sauvegarde
            
            messages.success(request, "Vidéo publiée avec succès !")
            return redirect('video_detail', video_id=video.id)
    else:
        # L'utilisateur arrive sur la page → formulaire vide
        form = VideoUploadForm()
    
    return render(request, 'video_upload.html', {'form': form})


@login_required
def video_edit(request, video_id):
    """
    Modifier une vidéo qu'on a publiée
    Seul le créateur peut modifier sa vidéo
    """
    video = get_object_or_404(Video, id=video_id)
    
    # Vérifier que c'est bien le propriétaire
    if video.creator != request.user:
        messages.error(request, "Vous ne pouvez pas modifier cette vidéo.")
        return redirect('video_detail', video_id=video.id)
    
    if request.method == 'POST':
        # instance=video → modifier la vidéo existante, pas en créer une nouvelle
        form = VideoEditForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Vidéo modifiée !")
            return redirect('video_detail', video_id=video.id)
    else:
        # Pré-remplir le formulaire avec les données actuelles
        form = VideoEditForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Vidéo modifiée !")
            return redirect('video_detail', video_id=video.id)
        else:
        # Pré-remplir le formulaire avec les données actuelles
            form = VideoEditForm(instance=video)
    
    return render(request, 'video_edit.html', {
        'form': form,
        'video': video,
    })


@login_required
def video_delete(request, video_id):
    """
    Supprimer une vidéo qu'on a publiée
    Avec confirmation avant suppression
    """
    video = get_object_or_404(Video, id=video_id)
    
    # Vérifier que c'est bien le propriétaire
    if video.creator != request.user:
        messages.error(request, "Action non autorisée.")
        return redirect('home')
    
    if request.method == 'POST':
        # L'utilisateur a confirmé la suppression
        video.delete()
        messages.success(request, "Vidéo supprimée.")
        return redirect('home')
    
    # Afficher la page de confirmation
    return render(request, 'video_delete.html', {'video': video})


@login_required
def video_like(request, video_id):
    """
    Liker ou unliker une vidéo
    Si déjà liké → unlike
    Si pas liké → like
    """
    video = get_object_or_404(Video, id=video_id)
    
    # get_or_create : essaie de trouver le like, sinon le crée
    like, created = Like.objects.get_or_create(user=request.user, video=video)
    
    if not created:
        # Le like existait déjà → on le supprime (unlike)
        like.delete()
    
    # Rediriger vers la page vidéo (l'utilisateur voit le like mis à jour)
    return redirect('video_detail', video_id=video.id)


def video_search(request):
    """
    Rechercher des vidéos par mot-clé dans le titre
    Exemple : /search/?q=chat
    """
    query = request.GET.get('q', '')  # Récupérer le mot recherché
    
    if query:
        # __icontains → insensible à la casse (Chat = chat)
        videos = Video.objects.filter(
            title__icontains=query,
            visibility='public'
        )
    else:
        # Pas de recherche → aucun résultat
        videos = Video.objects.none()
    
    return render(request, 'search_results.html', {
        'videos': videos,
        'query': query,
    })


def video_category(request, slug):
    """
    Afficher les vidéos d'une catégorie spécifique
    Exemple : /category/musique/
    """
    category = get_object_or_404(Category, slug=slug)
    videos = Video.objects.filter(category=category, visibility='public')
    
    return render(request, 'category.html', {
        'category': category,
        'videos': videos,
    })



def video_stream(request, video_id):
    """
    Sert la vidéo avec support des Range Requests (permet d'avancer/reculer)
    """
    video = get_object_or_404(Video, id=video_id)
    file_path = video.video_file.path
    
    # Taille du fichier
    file_size = os.path.getsize(file_path)
    
    # Récupérer le Range depuis les headers
    range_header = request.META.get('HTTP_RANGE', '').strip()
    
    if range_header:
        # Exemple : "bytes=0-1023"
        byte_range = range_header.split('=')[1]
        start, end = byte_range.split('-')
        start = int(start) if start else 0
        end = int(end) if end else file_size - 1
        
        # Lire la portion demandée
        length = end - start + 1
        
        with open(file_path, 'rb') as f:
            f.seek(start)
            data = f.read(length)
        
        response = HttpResponse(data, status=206, content_type='video/mp4')
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Content-Length'] = str(length)
        response['Accept-Ranges'] = 'bytes'
        
    else:
        # Pas de Range → envoyer tout le fichier
        with open(file_path, 'rb') as f:
            data = f.read()
        
        response = HttpResponse(data, content_type='video/mp4')
        response['Content-Length'] = str(file_size)
        response['Accept-Ranges'] = 'bytes'
    
    return response
