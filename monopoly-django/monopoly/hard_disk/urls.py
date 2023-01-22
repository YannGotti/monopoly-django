from django.urls import path
from . import views

urlpatterns = [
    path('disk/<int:pk>/', views.SelectDisk.as_view(), name='select_disk'),
    path('disk/client/getData/', views.ClientDataDisk.as_view()),
]