from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowAllPc.as_view()),
    path('pc/', views.AddPc.as_view(), name='add_pc'),
    path('pc/<int:pk>/', views.SelectPc.as_view(), name='pc'),
    path('pc/delete/<int:pk>/', views.DeletePc.as_view(), name='delete_pc'),

    path('pc/ajax/select_last_pc/', views.SelectLastPc.as_view(), name='select_last_pc'),

    path('pc/client/add_pc/', views.ClietAddPc.as_view()),
    path('pc/client/add_disk/', views.ClientAddHardDrive.as_view()),
    path('pc/client/info_disk/', views.ClientAddInfoDrive.as_view()),
    path('pc/client/getKey/', views.GetKeyPc.as_view()),

]