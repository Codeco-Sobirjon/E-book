from django.urls import path

from apps.e_book.register.views import register_view, login_view, logout_view
from apps.e_book.views import index, content_list_view, content_list_term_view, search_view, quiz_test, enter_page_view

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

    # quiz
    path("quiz/<int:subcategory_id>/", quiz_test, name="quiz_test"),

    # enter page
    path('enter_page/<int:id>/', enter_page_view, name='enter_page_view'),

]
