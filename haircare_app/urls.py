from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.welcome, name='welcome'),  # Головна сторінка (welcome)
    path('register/', views.register, name='register'),  # Реєстрація
    path('login/', views.user_login, name='login'),  # Вхід
    path('profile/', views.profile, name='profile'),  # Профіль
    path('home/', views.home, name='home'),  # Домашня сторінка
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/add/', views.journal_add, name='journal_add'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='accounts_login'),
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/add/', views.journal_add, name='journal_add'),
    path('journal/delete/<int:pk>/', views.journal_delete, name='journal_delete'),
    path('welcome/', views.welcome, name='welcome'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('assistant/', views.ai_assistant, name='ai_assistant'),
    path('accounts/', include('allauth.urls')),


    # Додатковий шлях для входу
]