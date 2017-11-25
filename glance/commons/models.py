# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# create and modified date for every item in the database.
class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')
    modified_date = models.DateTimeField(auto_now=True,
                                         verbose_name='修改时间')

    class Meta:
        abstract = True
