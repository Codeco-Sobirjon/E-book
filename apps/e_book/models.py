from xml.dom.minidom import Document
import os
import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=250, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="Parent Category", related_name='subcategories')
    is_test_page = models.BooleanField(default=False, null=True, blank=True, verbose_name="Test Page")
    is_enter_page = models.BooleanField(default=False, null=True, blank=True, verbose_name="Enter Page")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Publication Date")

    objects = models.Manager()

    def __str__(self):
        # Получаем переведённое имя
        str_name = getattr(self, 'name', "Untitled") or "Untitled"
        parent = self.parent

        while parent:
            parent_name = getattr(parent, 'name', "Untitled") or "Untitled"
            str_name = f'{parent_name} / {str_name}'
            parent = parent.parent

        return str_name

    class Meta:
        ordering = ["id"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class TopLevelCategory(Category):
    class Meta:
        proxy = True
        verbose_name = "1. Main Category"
        verbose_name_plural = "1. Main Categories"


class SubCategory(Category):
    class Meta:
        proxy = True
        verbose_name = "2. Subcategory"
        verbose_name_plural = "2. Subcategories"


class Content(models.Model):
    name = models.CharField(_("Name"), max_length=250, null=True, blank=True)
    time = models.CharField(_("Time"), max_length=250, null=True, blank=True)
    duration = models.CharField(_("Duration"), max_length=250, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Category',
                                 related_name='category')
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Publication Date")

    objects = models.Manager()

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "3. Contents"
        ordering = ['created_at']


class ContentText(models.Model):
    name = models.CharField(_("Name"), max_length=250, null=True, blank=True)
    description = RichTextField(verbose_name="Short Description")
    contentID = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True, related_name='content_text',
                                  verbose_name='Content')
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Publication Date")

    objects = models.Manager()

    class Meta:
        verbose_name = "Content Text"
        verbose_name_plural = "Content Texts"
        ordering = ['created_at']


class ContnetExamples(models.Model):
    name = models.CharField(_("Name"), max_length=250, null=True, blank=True)
    description = RichTextField(verbose_name="Short Description")
    contentID = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='content_example',
                                  verbose_name='Content')
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Publication Date")

    objects = models.Manager()

    class Meta:
        verbose_name = "Content Example"
        verbose_name_plural = "Content Examples"
        ordering = ['created_at']


class ContentResources(models.Model):
    name = models.CharField(_("Name"), max_length=250, null=True, blank=True)
    link = models.URLField(null=True, blank=True, verbose_name="Link")
    contentID = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='content_resource',
                                  verbose_name='Content')
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Publication Date")

    objects = models.Manager()

    class Meta:
        verbose_name = "Content Resource"
        verbose_name_plural = "Content Resources"
        ordering = ['created_at']


class ContentTerm(models.Model):
    name = models.CharField(_("Name"), max_length=250, null=True, blank=True)
    description = RichTextField(verbose_name="Short Description")
    contentID = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='content_term',
                                  verbose_name='Content')
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Publication Date")

    objects = models.Manager()

    class Meta:
        verbose_name = "Content Term"
        verbose_name_plural = "Content Terms"
        ordering = ['created_at']


class EnterPage(models.Model):
    name = models.CharField(_("Name"), max_length=250, null=True, blank=True)
    description = RichTextField(verbose_name="Short Description")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="enter_pages", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Publication Date")

    objects = models.Manager()

    class Meta:
        db_table = "e_book_enterpage"
        verbose_name = "Enter Page"
        verbose_name_plural = "4. Enter Pages"
        ordering = ['created_at']


class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Quiz Title"), null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="quizzes", null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.title or _("Unnamed Quiz")

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("5. Quizzes")


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", null=True, blank=True)
    text = models.CharField(max_length=500, verbose_name=_("Question Text"), null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.text or _("Unnamed Question")

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("6. Questions")


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", null=True, blank=True)
    text = models.CharField(max_length=300, verbose_name=_("Answer Text"), null=True, blank=True)
    is_correct = models.BooleanField(default=False, verbose_name=_("Is Correct"))

    objects = models.Manager()

    def __str__(self):
        return self.text or _("Unnamed Answer")

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


class Videos(models.Model):
    url_video = models.URLField(null=True, blank=True, verbose_name=_("Video URL"))

    objects = models.Manager()

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("7. Videos")


class LessonDevelopments(models.Model):
    name = models.CharField(_("Name"), max_length=250, null=True, blank=True)
    file = models.FileField(upload_to='lesson/', null=True, blank=True, verbose_name=_("Lesson File"))

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Lesson Development")
        verbose_name_plural = _("8. Lesson Developments")
