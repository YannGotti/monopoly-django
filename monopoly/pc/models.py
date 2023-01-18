from django.db import models

class UserPc(models.Model):
    ''' данные поста'''
    name = models.CharField('Имя компьютера', max_length=100)
    ip = models.CharField('IP компьютера', max_length=100)
    mac_adress = models.CharField('MAC компьютера', max_length=100)
    description = models.TextField('Информация о пк')
    date_connection = models.DateTimeField('Дата подключения', auto_now_add=True)

    def __str__(self):
        return f'{self.name}, {self.mac_adress}'

    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'