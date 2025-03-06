import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from apps.e_book.models import Category, Content, SubCategory, ContentTerm, ContentResources, Quiz, Question, Answer, \
    Videos, LessonDevelopments
from django.utils import translation
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Content, ContentResources


def custom_404(request, exception):
    return render(request, '404.html', status=404)


@login_required
def index(request):
    videos = Videos.objects.all()
    lesson_dev = LessonDevelopments.objects.all().order_by('id')
    context = {
        'videos': videos,
        'lesson_dev': lesson_dev
    }
    return render(request, 'index.html', context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)


@login_required
def content_list_view(request, *args, **kwargs):
    current_language = request.session.get('django_language', translation.get_language())
    translation.activate(current_language)

    instance = get_object_or_404(Category, id=kwargs.get('id'))
    instance_content = Content.objects.select_related('category').prefetch_related(
        'content_text', 'content_example', 'content_resource'
    ).filter(category=instance).first()

    context = {
        'instance_content': instance_content,
        'category': instance
    }
    return render(request, 'content.html', context)


@login_required
def content_list_term_view(request):
    categories = Category.objects.filter(parent__isnull=False).prefetch_related('subcategories')

    term_list = []
    for category in categories:
        terms = ContentTerm.objects.filter(contentID__category=category)
        term_list.append({'category': category, 'terms': terms})

    context = {
        'term_list': term_list,
    }
    return render(request, 'term.html', context)


@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse({"error": "Search query is required"}, status=400)

    content_results = Content.objects.filter(Q(name__icontains=query))
    content_resources_results = ContentResources.objects.filter(Q(name__icontains=query))

    content_data = [
        {
            "id": item.id,
            "name": item.name,
            "category_id": item.category.id if item.category else None  # Добавляем category_id
        }
        for item in content_results
    ]

    content_resources_data = [
        {
            "id": item.id,
            "name": item.name,
            "category_id": item.contentID.category.id if item.contentID and item.contentID.category else None
        }
        for item in content_resources_results
    ]

    return JsonResponse({
        "content": content_data,
        "content_resources": content_resources_data
    })


def quiz_test(request, subcategory_id):
    subcategory = get_object_or_404(Category, id=subcategory_id)

    quizzes = Quiz.objects.filter(category=subcategory)

    if not quizzes.exists():
        return render(request, "quiz/no_quizzes.html", {"subcategory": subcategory})

    quiz = quizzes.first()

    if request.method == "POST":
        total_questions = 10
        correct_answers = 0
        user_answers = {}

        for key, value in request.POST.items():
            if key.startswith("question_"):
                question_id = int(key.split("_")[1])
                selected_answer_id = int(value)
                user_answers[question_id] = selected_answer_id

                if Answer.objects.filter(id=selected_answer_id, is_correct=True).exists():
                    correct_answers += 1

        score_percentage = (correct_answers / total_questions) * 100
        wrong_answers = total_questions - correct_answers

        return render(request, "quiz/quiz_results.html", {
            "quiz": quiz,
            "subcategory": subcategory,
            "correct_answers": correct_answers,
            "wrong_answers": wrong_answers,
            "score_percentage": score_percentage,
        })

    questions = list(Question.objects.filter(quiz=quiz).order_by('?')[:10])

    for question in questions:
        question.answers_list = list(question.answers.all())
        random.shuffle(question.answers_list)  # Shuffle answers

    return render(request, "quiz/quiz_test.html", {
        "subcategory": subcategory,
        "quiz": quiz,
        "questions": questions
    })
