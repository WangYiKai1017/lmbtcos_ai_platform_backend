from django.db import models
from django.contrib.auth.models import User


class SliceFile(models.Model):
    """
    切片文件模型
    """
    STATUS_CHOICES = [
        ('uploaded', '已上传'),
        ('processed', '已处理'),
        ('failed', '处理失败'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255, verbose_name='文件名')
    type = models.CharField(max_length=100, verbose_name='文件类型')
    size = models.BigIntegerField(verbose_name='文件大小')
    uploaded = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded', verbose_name='状态')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='上传者')
    file_path = models.CharField(max_length=500, verbose_name='文件路径')
    
    class Meta:
        verbose_name = '切片文件'
        verbose_name_plural = '切片文件'
        ordering = ['-uploaded']
    
    def __str__(self):
        return self.name


class SlicePage(models.Model):
    """
    文档页面模型
    """
    id = models.CharField(max_length=50, primary_key=True)
    file_id = models.ForeignKey(SliceFile, on_delete=models.CASCADE, related_name='pages', verbose_name='所属文件')
    page_number = models.IntegerField(verbose_name='页码')
    content = models.TextField(blank=True, null=True, verbose_name='页面内容预览')
    selected = models.BooleanField(default=False, verbose_name='是否选中')
    
    class Meta:
        verbose_name = '文档页面'
        verbose_name_plural = '文档页面'
        ordering = ['page_number']
    
    def __str__(self):
        return f"Page {self.page_number} of {self.file_id.name}"


class SliceResult(models.Model):
    """
    切片结果模型
    """
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '处理失败'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    file_id = models.ForeignKey(SliceFile, on_delete=models.CASCADE, related_name='results', verbose_name='所属文件')
    page_ids = models.TextField(verbose_name='处理的页面ID列表')
    processed_content = models.TextField(blank=True, null=True, verbose_name='处理后的内容')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    
    class Meta:
        verbose_name = '切片结果'
        verbose_name_plural = '切片结果'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Result {self.id} for {self.file_id.name}"
