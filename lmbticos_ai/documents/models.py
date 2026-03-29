from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    """
    文档模型，用于表示文件或文件夹
    """
    TYPE_CHOICES = [
        ('file', '文件'),
        ('folder', '文件夹'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255, verbose_name='名称')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='类型')
    icon = models.CharField(max_length=10, verbose_name='图标')
    size = models.CharField(max_length=20, blank=True, null=True, verbose_name='大小')
    modified = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    parent_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='父文件夹ID')
    
    # 文件特有字段
    file_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='文件类型')
    content_type = models.CharField(max_length=100, blank=True, null=True, verbose_name='内容类型')
    file_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='文件路径')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='上传者')
    access_level = models.CharField(max_length=20, default='public', verbose_name='访问级别')
    
    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档'
        ordering = ['-modified']
    
    def __str__(self):
        return f"{self.name} ({self.type})"
