from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """
    文档序列化器
    """
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'modified', 'uploaded_by']
    
    def validate(self, data):
        """
        验证数据
        """
        # 如果是文件类型，必须提供file_type、content_type等字段
        if data['type'] == 'file':
            required_fields = ['file_type', 'content_type', 'file_path']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(f"{field} 是文件类型的必填字段")
        
        # 如果是文件夹类型，不能提供文件特有字段
        if data['type'] == 'folder':
            file_fields = ['file_type', 'content_type', 'file_path']
            for field in file_fields:
                if field in data:
                    raise serializers.ValidationError(f"{field} 不适用于文件夹类型")
        
        return data
