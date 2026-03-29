from rest_framework import serializers
from .models import SliceFile, SlicePage, SliceResult


class SliceFileSerializer(serializers.ModelSerializer):
    """
    切片文件序列化器
    """
    class Meta:
        model = SliceFile
        fields = '__all__'
        read_only_fields = ['id', 'uploaded', 'status', 'uploaded_by']


class SlicePageSerializer(serializers.ModelSerializer):
    """
    文档页面序列化器
    """
    class Meta:
        model = SlicePage
        fields = '__all__'
        read_only_fields = ['id', 'file_id']


class SliceResultSerializer(serializers.ModelSerializer):
    """
    切片结果序列化器
    """
    class Meta:
        model = SliceResult
        fields = '__all__'
        read_only_fields = ['id', 'file_id', 'created_at', 'completed_at', 'status']
    
    def validate_page_ids(self, value):
        """
        验证页面ID列表
        """
        if not value:
            raise serializers.ValidationError("页面ID列表不能为空")
        return value
