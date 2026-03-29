from django.urls import path
from . import views

urlpatterns = [
    # 获取文件系统树
    path('', views.get_file_system_tree, name='get_file_system_tree'),
    
    # 创建文件夹
    path('folders/', views.create_folder, name='create_folder'),
    
    # 上传文件
    path('files/', views.upload_file, name='upload_file'),
    
    # 获取文件详情
    path('files/<str:file_id>/', views.get_file_detail, name='get_file_detail'),
    
    # 删除文件/文件夹
    path('<str:id>/', views.delete_file_or_folder, name='delete_file_or_folder'),
]