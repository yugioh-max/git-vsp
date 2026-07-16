from django.contrib import admin
from .models import Video, Category
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  #slug auto

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'visibility', 'created_at']