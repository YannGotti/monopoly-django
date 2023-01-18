from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowAllPc.as_view()),
    path('pc/', views.AddPc.as_view(), name='add_pc'),
    path('pc/<int:pk>/', views.SelectPc.as_view(), name='pc'),
    path('pc/delete/<int:pk>', views.DeletePc.as_view(), name='delete_pc')
]