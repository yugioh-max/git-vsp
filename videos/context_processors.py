from .models import Category

def categories_processor(request):
    """
    Rend les catégories disponibles dans tous les templates
    """
    return {
        'all_categories': Category.objects.all()
    }