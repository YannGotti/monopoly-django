from django.db import models

class UserPc(models.Model):
    ''' данные поста'''
    name = models.CharField('Имя компьютера', max_length=100)
    ip = models.CharField('IP компьютера', max_length=100)
    mac_adress = models.CharField('MAC компьютера', max_length=100)
    description = models.TextField('Информация о пк')
    date_connection = models.DateTimeField('Дата подключения', auto_now_add=True)
    on_active = models.BooleanField('Активен ли', default=False)

    def __str__(self):
        return f'{self.name}, {self.mac_adress}'

    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'


class Disk(models.Model):
    ''' данные диска'''
    name = models.CharField('Имя диска', max_length=100)
    full_name = models.CharField('Полное имя компьютера', max_length=100)
    serial_number = models.CharField('Серийный номер', max_length=100)
    range = models.IntegerField('Объем диска')
    user_pc = models.ForeignKey(UserPc, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.serial_number}'

    class Meta:
        verbose_name = 'Диск'
        verbose_name_plural = 'Диски'