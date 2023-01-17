from django.db import models

class Post(models.Model):
    ''' данные о посте'''
    title = models.CharField('Заголовок записи', max_length=100)
    description = models.TextField('Текст записи')
