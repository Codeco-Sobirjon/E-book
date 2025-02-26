from apps.e_book.models import Category
from django.utils import translation


def categories_processor(request):
    current_language = request.session.get('django_language', translation.get_language())
    translation.activate(current_language)
    get_main_category = Category.objects.filter(
        parent__isnull=True
    ).prefetch_related('subcategories')
    return {'categories': get_main_category}
