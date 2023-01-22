from django.urls import path
from . import views

urlpatterns = [
    path('disk/<int:pk>/', views.SelectDisk.as_view(), name='select_disk'),
    path('disk/<int:pk>/clear/', views.MainFolderSelect.as_view(), name='select_main_folder'),

    path('disk/<int:pk>/updateData/', views.GetPathFolder.as_view(), name='update_data'),

    path('disk/client/getData/', views.ClientDataDisk.as_view()),
    path('disk/client/getRequest/', views.ClientGetRequest.as_view()),
    path('disk/client/postRequestState/', views.ClientGetStateRequest.as_view()),
]