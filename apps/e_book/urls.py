from django.urls import path

from apps.e_book.register.views import register_view, login_view, logout_view
from apps.e_book.views import index, content_list_view, content_list_term_view, search_view, start_quiz_view, \
    get_questions, get_answer, get_finish, start_quiz_questions, show_answer

urlpatterns = [
    path('', login_view, name='login'),
    path('home', index, name='home'),

    # register
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # content
    path('content/list/<int:id>/', content_list_view, name='content_list_view'),
    path('content/list/term/', content_list_term_view, name='content_list_term_view'),

    # search json responce
    path('search/', search_view, name='search'),

    path('quiz/start/<int:category_id>/', start_quiz_view, name='start_quiz'),
    path('quiz/questions/<int:quiz_id>/', get_questions, name='get_questions'),
    path('quiz/questions/start/', start_quiz_questions, name='start_questions'),
    path('quiz/answer/', get_answer, name='get_answer'),
    path('quiz/answer/<int:quiz_id>/', show_answer, name='show_answer'),  # Новая страница показа ответа
    path('quiz/finish/', get_finish, name='get_finish'),

]
print(lambda request: get_questions(request, is_start=True))
