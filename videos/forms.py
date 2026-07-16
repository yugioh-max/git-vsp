import os

from django import forms
from django.core.exceptions import ValidationError
from .models import Video

class VideoUploadForm(forms.ModelForm):
    """
    Formulaire pour uploader une nouvelle vidéo
    """
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail', 'category', 'visibility']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Décrivez votre vidéo...'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Titre de la vidéo'
            }),
            'video_file': forms.FileInput(attrs={
                'class':'form-file'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-file'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'visibility': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_video_file(self):
        """Verifie que le fichier uploadé est bien une vidéo"""
        video = self.cleaned_data.get('video_file')

        if video:
            allowed_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']
            ext = os.path.splitext(video.name)[1].lower()

            if ext not in allowed_extensions:
                raise ValidationError(f"Format non supporté. Format accepté: {', '.join(allowed_extensions)}")
            
            max_size = 3 * 1024 * 1024 * 1024
            if video.size > max_size:
                raise ValidationError("La vidéo ne doit pas dépasser 3Go.")
            
        return video
    
    def clean_thumbnail(self):
        """Vérifie que la miniature est une image"""
        thumbnail = self.cleaned_data.get('thumbnail')

        if thumbnail:
            allowed_extensions = ['.jpg', '.jpeg', '.png', 'webp']
            ext = os.path.splitext(thumbnail.name)[1].lower()

            if ext not in allowed_extensions:
                raise ValidationError(f"Format d'image non supporté. Formats accepté: {', '.join(allowed_extensions)}")
            
        return thumbnail
    
        


class VideoEditForm(forms.ModelForm):
    """
    Formulaire pour modifier une vidéo existante
    Pas de champ video_file car on ne change pas la vidéo elle-même
    """
    class Meta:
        model = Video
        fields = ['title', 'description', 'thumbnail', 'category', 'visibility']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Titre de la vidéo'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-file'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'visibility': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
       

