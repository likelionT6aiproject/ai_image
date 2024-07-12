from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_image, name='upload_image'),
    path('result/<int:pk>/', views.view_result, name='result'),
]
