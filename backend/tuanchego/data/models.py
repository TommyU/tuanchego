from django.db import models

# Create your models here.
class BaseModel(models.Model):
    """
    BaseModel基础模型
    """
    created_time = models.DateTimeField(verbose_name=u'记录创建时间', auto_now_add=True, blank=True, null=True)
    updated_time = models.DateTimeField(verbose_name=u'记录上次更新时间', auto_now=True, blank=True, null=True)
    memo = models.CharField(max_length=128, null=True,blank=True, verbose_name=u'备注')
    class Meta:
        abstract = True

class City(BaseModel):
    """
   	城市
    """
    initial = models.CharField(max_length=1,null = True, blank=True,index=True, verbose_name=u'首字母' )
    name = models.CharField(max_length=64, null = True, blank=True,   verbose_name=u'名称' )
    sequence =  models.IntegerField(null=True, default=0, verbose_name=u'排序')
    is_hot = models.BooleanField(null = True, blank=True,  verbose_name=u'是否热门' )
    
    def __str__(self):
        return self.name

class SysParam(BaseModel):
    """
    系统参数
    """
    key = models.CharField(max_length=64, null=True, blank=True, verbose_name=u'键')
    value = models.CharField(max_length=256,null=True, blank=True, verbose_name=u'值')

    def __str__(self):
        return self.key

class Content(BaseModel):
    """
    内容页
    """
    title = models.CharField(max_length=256, index=True, null=True, blank=True, verbose_name=u'标题' )
    content = models.TextField(null=True,blank=True, verbose_name=u'内容')
    uri = models.CharField(max_length=32, null=True, blank=True ,index=True, verbose_name=u'短地址')
    status = models.CharField(max_length=16, null=True, blank=True, index=True, verbose_name=u'状态',
        choices=[('draft',u'草稿'), ('published',u'已发布')], default='draft'
        )
    def __str__(self):
        return self.title or '(no title)'

class Links(BaseModel):
    """
    链接
    """
    position = models.CharField(max_length=32, null=true, blank=True, verbose_name=u'页面位置')
    link_type = models.CharField(max_length=32, null=True, blank=True, verbose_name=u'用途')
    target_url = models.CharField(max_length=256, null=True, blank=True, verbose_name=u'目标跳转地址')
    content_text = models.CharField(max_length=128, null=True, blank=true, verbose_name=u'链接文本内容')
    img_url = models.CharField(max_length=256, null=True, blank=True, verbose_name=u'链接图片资源地址')
    city = models.ForeignKey(City, null=True,blank=True, verbose_name=u'城市')

    def __str__(self):
        return self.content_text or '(no content text)'
