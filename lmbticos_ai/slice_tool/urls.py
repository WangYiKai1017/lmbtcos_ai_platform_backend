from django.urls import path
from . import views

urlpatterns = [
    # 上传切片文件
    path('files/', views.upload_slice_file, name='upload_slice_file'),
    
    # 获取上传文件列表
    path('files/', views.get_upload_files, name='get_upload_files'),
    
    # 获取文档页面
    path('files/<str:file_id>/pages/', views.get_document_pages, name='get_document_pages'),
    
    # 开始切片处理
    path('files/<str:file_id>/process/', views.start_slice_process, name='start_slice_process'),
    
    # 获取切片结果
    path('results/<str:result_id>/', views.get_slice_result, name='get_slice_result'),
]