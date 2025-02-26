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


def start_quiz_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    quizzes = Quiz.objects.filter(category=category).annotate(questions_count=Count('questions'))
    quiz_get = quizzes.first()
    return render(request, 'quiz/start_quiz.html', context={'topics': quizzes, 'quiz_get': quiz_get})


def start_quiz_questions(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    quiz_id = request.POST.get('quiz_id')
    if not quiz_id:
        return HttpResponseBadRequest("Quiz ID is missing.")

    _reset_quiz(request)
    request.session['last_quiz_id'] = quiz_id
    question = _get_first_question(quiz_id)

    if question is None:
        return redirect('get_finish')

    request.session['question_id'] = question.id
    return redirect('get_questions', quiz_id=quiz_id)


def _get_first_question(quiz_id):
    return Question.objects.filter(quiz_id=quiz_id).order_by('id').first()


def get_questions(request, quiz_id):
    question = _get_subsequent_question(request, quiz_id)
    request.session['last_quiz_id'] = quiz_id
    if question is None:
        return redirect('get_finish')

    request.session['question_id'] = question.id
    answers = Answer.objects.filter(question=question).order_by("?")

    return render(request, 'quiz/question.html', context={
        'question': question, 'answers': answers
    })


def _get_subsequent_question(request, quiz_id):
    previous_question_id = request.session.get('question_id')
    if previous_question_id is None:
        return None

    next_question = Question.objects.filter(
        quiz_id=quiz_id, id__gt=previous_question_id
    ).order_by('id').first()
    return next_question


def get_answer(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    submitted_answer_id = request.POST.get('answer_id')
    if not submitted_answer_id:
        return HttpResponseBadRequest("Answer ID is missing.")

    submitted_answer = get_object_or_404(Answer, id=submitted_answer_id)
    question = submitted_answer.question
    quiz_id = question.quiz.id

    if submitted_answer.is_correct:
        request.session['score'] = request.session.get('score', 0) + 1

    correct_answer = Answer.objects.filter(question=question, is_correct=True).first()

    request.session['last_question_id'] = question.id
    request.session['last_answer_id'] = submitted_answer.id

    return redirect('show_answer', quiz_id=quiz_id)


def show_answer(request, quiz_id):
    question_id = request.session.get('last_question_id')
    answer_id = request.session.get('last_answer_id')

    question = get_object_or_404(Question, id=question_id)
    submitted_answer = get_object_or_404(Answer, id=answer_id)
    correct_answer = Answer.objects.filter(question=question, is_correct=True).first()

    return render(request, 'quiz/answer.html', context={
        'question': question,
        'submitted_answer': submitted_answer,
        'correct_answer': correct_answer,
        'quiz_id': quiz_id
    })


def get_finish(request):
    score = request.session.get('score', 0)
    quiz_id = request.session.get('last_quiz_id')

    if quiz_id:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions_count = Question.objects.filter(quiz=quiz).count()
    else:
        questions_count = 1

    percent = max(0, min(100, int((score / max(questions_count, 1)) * 100)))

    _reset_quiz(request)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    return render(request, 'quiz/finish.html', context={
        'questions_count': questions_count, 'score': score, 'percent_score': percent, 'quiz_id': quiz.category.id
    })


def _reset_quiz(request):
    request.session.pop('question_id', None)
    request.session.pop('score', None)
    request.session.pop('last_question_id', None)
    request.session.pop('last_answer_id', None)
    return request
