from django.urls import path
from . import views

urlpatterns = [
    # 创建对话会话
    path('conversations/', views.create_conversation, name='create_conversation'),
    
    # 获取对话消息列表
    path('conversations/<str:session_id>/messages/', views.get_conversation_messages, name='get_conversation_messages'),
    
    # 发送对话消息
    path('conversations/<str:session_id>/messages/', views.send_conversation_message, name='send_conversation_message'),
    
    # 生成故事卡
    path('conversations/<str:session_id>/generate-cards/', views.generate_cards, name='generate_cards'),
]