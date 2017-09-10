# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CurriculumDay, Curriculum


class CurriculumInline(admin.TabularInline):
    model = Curriculum
    extra = 0


@admin.register(CurriculumDay)
class CurriculumDayAdmin(admin.ModelAdmin):
    inlines = (CurriculumInline, )