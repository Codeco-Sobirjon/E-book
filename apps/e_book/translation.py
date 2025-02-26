from modeltranslation.translator import register, TranslationOptions
from apps.e_book.models import (
    Category, TopLevelCategory, SubCategory,
    Content, ContentText, ContentResources, ContnetExamples, ContentTerm, Quiz, Question, Answer, LessonDevelopments
)


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name',)


@register(TopLevelCategory)
class TopLevelCategoryTranslation(TranslationOptions):
    fields = ('name',)


@register(SubCategory)
class SubCategoryTranslation(TranslationOptions):
    fields = ('name',)


@register(Content)
class ContentTranslation(TranslationOptions):
    fields = ['name', 'time', 'duration']


@register(ContentText)
class ContentTextTranslation(TranslationOptions):
    fields = ['name', 'description']


@register(ContentTerm)
class ContentTermTranslation(TranslationOptions):
    fields = ['name', 'description']


@register(ContnetExamples)
class ContnetExamplesTranslation(TranslationOptions):
    fields = ['name', 'description']


@register(ContentResources)
class ContentResourcesTranslation(TranslationOptions):
    fields = ['name']


@register(Quiz)
class QuizTranslation(TranslationOptions):
    fields = ['title']


@register(Question)
class QuestionTranslation(TranslationOptions):
    fields = ['text']


@register(Answer)
class AnswerTranslation(TranslationOptions):
    fields = ['text']


@register(LessonDevelopments)
class LessonDevelopmentsTranslation(TranslationOptions):
    fields = ['name']
