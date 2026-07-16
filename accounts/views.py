from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile

def register_view(request):
    """Inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer le profil automatiquement
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Compte créé avec succès !")
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Connexion"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.username} !")
                
                # Rediriger vers la page demandée ou l'accueil
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('home')


@login_required
def profile_view(request):
    """Voir/modifier son profil"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour !")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})


def public_profile_view(request, username):
    """Voir le profil public d'un utilisateur"""
    from django.shortcuts import get_object_or_404
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    profile_user = get_object_or_404(User, username=username)
    videos = profile_user.videos.filter(visibility='public')
    
    return render(request, 'public_profile.html', {
        'profile_user': profile_user,
        'videos': videos,
    })
