
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('Files/', views.fileList.as_view()),
    path('return-key/My_Key.pem', views.return_key, name='return_key'),
    path('return-file/', views.return_file, name='return_file'),
    #path('home/download', views.downloads, name='downloads'),
    path('download/', views.downloads, name='downloads'),
    path('upload/', views.call_page_upload, name='call_page_upload'),
    path('', views.back_home, name='back_home'),
    path('data', views.upload_file, name='upload_file'),
    path('download_data', views.upload_key, name='upload_key'),

]
