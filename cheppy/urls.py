from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('course/', views.course, name='course'),
    path('coding/', views.coding, name='coding'),
    path('solution/', views.solution, name='solution'),
    path('survey/', views.survey, name='survey'),
    path('test_page/', views.test_page, name='test_page'),
]