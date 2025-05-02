from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('init_pdf/', views.InitialPdf.as_view()),
    path('chat/', views.ChatView.as_view()),
]