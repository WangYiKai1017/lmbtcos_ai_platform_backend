"""
Agents API应用配置
"""

from django.apps import AppConfig


class AgentsApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agents_api'
    verbose_name = 'Agents API'
