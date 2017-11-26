# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from commons.models import Timestampable
from django.utils.translation import ugettext_lazy as _


class SerialManager(models.Manager):

    def is_exist(self, serial):
        return True if self.get_queryset().filter(serial=serial) else False


class Serial(Timestampable, models.Model):
    """平台序列会员表"""
    serial = models.CharField(max_length=32, unique=True, db_index=True,
                              verbose_name='序列会员号')
    is_supper = models.BooleanField(default=False, verbose_name='超级会员')
    level = models.PositiveSmallIntegerField(verbose_name='会员层级')
    name = models.CharField(max_length=32, unique=True, verbose_name='会员姓名')
    moblie = models.CharField(max_length=12, unique=True, verbose_name='手机号')
    #  Links Serial to a User model instance.
    user = models.OneToOneField(User)
    objects = SerialManager()

    class Meta:
        verbose_name = _('序列会员')
        verbose_name_plural = _('序列会员')

    def __unicode__(self):
        return self.serial

    def save(self, **kwargs):
        # 根据serial长度决定会员层级,前3位为地区码,后每两位一层
        self.level = (len(self.serial) - 3) / 2
        super(Serial, self).save(kwargs)


class Member(Timestampable, models.Model):
    """平台用户表"""
    name = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    email = models.EmailField(unique=True, verbose_name='注册邮箱')
    moblie = models.CharField(max_length=12, unique=True, verbose_name='手机号')
    # 默认使用 01001这个序列号
    serial = models.CharField(max_length=32, default="01001", null=True,
                              db_index=True, verbose_name='序列号')
    serial_changed = models.IntegerField(default=0, verbose_name='序列号改变次数')
    uid = models.CharField(max_length=32, unique=True,
                           verbose_name='优宜巧购用户ID')
    reg_time = models.DateTimeField(verbose_name='优宜巧购注册时间')

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        # 当序列号变动，serial_changed +1
        previous = Member.objects.filter(pk=self.pk).first()
        if previous:
            if previous.serial != self.serial:
                self.serial_changed += 1
        super(Member, self).save(kwargs)


class Order(Timestampable, models.Model):
    """平台完成订单表"""
    order_number = models.IntegerField(unique=True, verbose_name='优宜巧购订单号')
    buyer_id = models.CharField(max_length=32, verbose_name='买家ID')
    buyer_name = models.CharField(max_length=32, verbose_name='买家名')
    total = models.FloatField(verbose_name='订单总金额')
    order_time = models.DateTimeField(verbose_name='下单时间')
    finished_time = models.DateTimeField(verbose_name='完成时间')

    class Meta:
        verbose_name = _('订单')
        verbose_name_plural = _('订单')

    def __unicode__(self):
        return unicode(self.order_number)