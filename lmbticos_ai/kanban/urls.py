from django.urls import path
from . import views

urlpatterns = [
    # 获取泳道列表
    path('swimlanes/', views.get_swimlanes, name='get_swimlanes'),
    
    # 获取故事卡列表
    path('cards/', views.get_cards, name='get_cards'),
    
    # 创建故事卡
    path('cards/', views.create_card, name='create_card'),
    
    # 更新故事卡状态
    path('cards/<str:card_id>/status/', views.update_card_status, name='update_card_status'),
]