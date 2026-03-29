from django.urls import path
from . import views

urlpatterns = [
    # 获取技能分类列表
    path('categories/', views.get_skill_categories, name='get_skill_categories'),
    
    # 获取技能列表
    path('', views.get_skills, name='get_skills'),
    
    # 获取技能详情
    path('<str:skill_id>/', views.get_skill_detail, name='get_skill_detail'),
]