from rest_framework import serializers
from .models import ModelRouter, Model


class ModelSerializer(serializers.ModelSerializer):
    """
    模型序列化器
    """
    class Meta:
        model = Model
        fields = '__all__'
        read_only_fields = ['id']


class ModelRouterSerializer(serializers.ModelSerializer):
    """
    模型路由器序列化器
    """
    models = ModelSerializer(many=True, read_only=True)
    
    class Meta:
        model = ModelRouter
        fields = '__all__'
        read_only_fields = ['id', 'lastUpdated']
    
    def validate_baseUrl(self, value):
        """
        验证基础URL
        """
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("基础URL必须以http://或https://开头")
        return value
