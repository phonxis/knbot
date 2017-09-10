# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import time

from django.db import models


TIMES = (
    (time(9,00), '09:00:00'),
    (time(10,30), '10:30:00'),
    (time(12,20), '12:20:00'),
    (time(13,50), '13:50:00'),
    (time(15,20), '15:20:00')
)
SUBJECTS =(
    ('Математичні та імітаційні моделі складних систем',
     'Математичні та імітаційні моделі складних систем'),
    ('Прикладна теорія графів',
     'Прикладна теорія графів'),
    ('Інформаційно-управляючі системи і технології в будівництві',
     'Інформаційно-управляючі системи і технології в будівництві'),
    ('Моделі і методи управління проектами',
     'Моделі і методи управління проектами'),
    ('Охорона праці в галузі',
     'Охорона праці в галузі'),
    ('Інформаційне моделювання технологій і бізнес-процесів в будівництві',
     'Інформаційне моделювання технологій і бізнес-процесів в будівництві'),
    ('Мережні технології',
     'Мережні технології')
)
TYPES = (
    ('Лекція', 'Лекція'),
    ('Лаба', 'Лаба'),
    ('Практика', 'Практика')
)
TEACHERS = (
    ('Ізмайлова О.В.', 'Ізмайлова О.В.'),
    ('Цюцюра С.В.', 'Цюцюра С.В.'),
    ('Касьянов Н.А.', 'Касьянов Н.А.'),
    ('Котетунов В.Ю.', 'Котетунов В.Ю.'),
    ('Бородавка Є.В.', 'Бородавка Є.В.'),
    ('Шутовський О.М.', 'Шутовський О.М.'),
    ('Невідомо', 'Невідомо')
)



class CurriculumDay(models.Model):
    day = models.DateField("Навчальний день",
                           unique=True)

    class Meta:
        verbose_name = "Навчальний день"
        verbose_name_plural = "Навчальні дні"

    def __unicode__(self):
        return self.day.isoformat()


class Curriculum(models.Model):
    day = models.ForeignKey(CurriculumDay,
                            related_name="subjects")
    time = models.TimeField("Час початку заняття",
                            choices=TIMES)
    subject = models.CharField("Назва пари",
                               max_length=128,
                               choices=SUBJECTS)
    type = models.CharField("Тип заняття",
                            max_length=32,
                            choices=TYPES,
                            default='lection')
    auditory = models.CharField("Аудиторія",
                                max_length=16)
    teacher = models.CharField("Викладач",
                               max_length=128,
                               choices=TEACHERS)

    class Meta:
        verbose_name = "Заняття"
        verbose_name_plural = "Заняття"
        unique_together = ('day', 'time')

    def __unicode__(self):
        return self.subject
