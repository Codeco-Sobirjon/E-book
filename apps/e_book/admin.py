from django.contrib import admin
from apps.e_book.models import (
    Category, TopLevelCategory, SubCategory,
    Content, ContentText, ContentResources, ContnetExamples, ContentTerm,
    Quiz, Question, Answer, Videos, LessonDevelopments, EnterPage
)


@admin.register(TopLevelCategory)
class TopLevelCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('translations__name',)
    list_filter = ('created_at',)
    exclude = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=True)

    def name(self, obj):
        try:
            return obj.safe_translation_getter('name', any_language=True) or 'Безымянный'
        except AttributeError:
            return getattr(obj, 'name', 'Безымянный')

    name.short_description = 'Название категория'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None or obj.parent is None:
            form.base_fields.pop('parent', None)
        return form


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    search_fields = ('translations__name', 'parent__translations__name')
    list_filter = ('parent', 'created_at')
    exclude = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=False, parent__parent__isnull=True)

    def name(self, obj):
        try:
            return obj.safe_translation_getter('name', any_language=True) or 'Безымянный'
        except AttributeError:
            return getattr(obj, 'name', 'Безымянный')

    name.short_description = 'Название подкатегория'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ContentTextInline(admin.TabularInline):
    model = ContentText
    extra = 1
    exclude = ('name', 'description')


class ContnetExamplesInline(admin.TabularInline):
    model = ContnetExamples
    extra = 1
    exclude = ('name', 'description')


class ContentResourcesInline(admin.TabularInline):
    model = ContentResources
    extra = 1
    exclude = ('name',)


class ContentTermInline(admin.TabularInline):
    model = ContentTerm
    extra = 1
    exclude = ('name', 'description')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'time', 'duration', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'category')
    inlines = [ContentTextInline, ContnetExamplesInline, ContentResourcesInline, ContentTermInline]
    exclude = ('name', 'time', 'duration')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=False, is_enter_page=False, is_test_page=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контенты"


@admin.register(EnterPage)
class EnterPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=False, is_enter_page=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    exclude = ('text',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title',)
    exclude = ('title',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=False, is_test_page=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text',)
    list_filter = ('quiz',)
    exclude = ('text',)
    inlines = [AnswerInline]


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = ("id", "url_video")
    search_fields = ("url_video",)


@admin.register(LessonDevelopments)
class LessonDevelopmentsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "file")
    search_fields = ("name",)
    list_filter = ("name",)
    exclude = ('name', )
