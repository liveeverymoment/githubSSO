"""
Model schema file
"""
from django.db import models

# Create your models here.
class CustomerOptions(models.Model):
    """
    CustomerOption model schema
    """
    key=models.CharField(max_length=30,default='oauthserver')
    value=models.CharField(max_length=30,default='github')

    class Meta:
        ordering=['key']
        verbose_name='customer options'

    def __str__(self) -> str:
        return str(self.key)
    
class Oidcclient(models.Model):
    """
    OAuth parameter schema model
    """
    choices=[
        ('github','Github'),
    ]
    application_name=models.CharField(max_length=50)
    client_id=models.CharField(max_length=30)
    client_secret=models.CharField(max_length=50)
    oauthserver=models.CharField(choices=choices,max_length=15,default='github')
    authorization_endpoint=models.URLField()
    token_endpoint=models.URLField()
    enduserinfo_endpoint=models.URLField()
    scope=models.JSONField()
    redirect_uri=models.URLField()
    response_type=models.CharField(max_length=30)

    class Meta:
        ordering=['application_name']
    
    def __str__(self) -> str:
        return str(self.application_name)
