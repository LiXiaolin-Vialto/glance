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
    mobile = models.CharField(max_length=12, unique=True, verbose_name='手机号')
    #  Links Serial to a User model instance.
    user = models.OneToOneField(User)
    objects = SerialManager()

    class Meta:
        verbose_name = _('序列会员')
        verbose_name_plural = _('序列会员')

    def __unicode__(self):
        return self.serial

    def save(self, **kwargs):
        s_len = len(self.serial.rstrip("0"))
        if (s_len == 5):
            self.level = 0
        elif (s_len == 6):
            self.level = 1
        else:
            self.level = 2
        super(Serial, self).save(kwargs)

    def get_subserial(self, include=True):
        """
        获取subserial, 是否包括自己.
        """
        # 超级serial
        if self.is_supper:
            if include:
                return Serial.objects.all()
            return Serial.objects.all().exclude(serial=self.serial)
        # 其他serial
        if self.is_supper:
            return Member.objects.all()
        if self.level == 0:
            condition = self.serial[:5]
        elif self.level == 1:
            condition = self.serial[:6]
        else:
            condition = self.serial
        sql = "serial LIKE '{}%%'".format(condition)
        if include:
            return Serial.objects.extra(where=[sql])
        return Serial.objects.extra(
            where=[sql]).exclude(serial=self.serial)

    def is_subserial_of(self, serial_obj):
        if serial_obj.is_supper:
            return True
        return (self in serial_obj.get_subserial())

    def managed_members(self):
        if self.is_supper:
            return Member.objects.all()
        pool = [s.serial for s in self.get_subserial()]
        return Member.objects.filter(serial__in=pool)


class MemberManager(models.Manager):

    def is_exist(self, mobile):
        return True if self.get_queryset().filter(mobile=mobile) else False


class Member(Timestampable, models.Model):
    """平台用户表"""
    name = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    email = models.EmailField(unique=True, verbose_name='注册邮箱')
    mobile = models.CharField(max_length=12, unique=True, verbose_name='手机号')
    # 默认使用 01001000这个序列号
    serial = models.CharField(max_length=32, default="01001000", null=True,
                              db_index=True, verbose_name='序列号')
    serial_changed = models.IntegerField(default=0, verbose_name='序列号改变次数')
    serial_history = models.TextField(default="=>", verbose_name='序列号改变历史')
    uid = models.CharField(max_length=32, unique=True,
                           verbose_name='优宜巧购用户ID')
    reg_time = models.DateTimeField(verbose_name='优宜巧购注册时间')
    objects = MemberManager()

    class Meta:
        verbose_name = _('优宜巧购用户')
        verbose_name_plural = _('优宜巧购用户')

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        # 当序列号变动，serial_changed +1
        previous = Member.objects.filter(pk=self.pk).first()
        if previous:
            if previous.serial != self.serial:
                self.serial_changed += 1
                self.serial_history += ("%s=>" % previous.serial)
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


class MonthlyData(Timestampable, models.Model):
    """优宜巧购用户月度消费表"""
    # 月度数据用YYYY-MM的字符形式
    month = models.CharField(max_length=16, verbose_name='月度')
    buyer_id = models.CharField(max_length=32, verbose_name='买家ID')
    buyer_name = models.CharField(max_length=32, verbose_name='买家名')
    total = models.FloatField(verbose_name='订单总金额')
    amount = models.IntegerField(verbose_name='优宜巧购月度订单数')

    class Meta:
        verbose_name = _('巧购用户月度订单汇总')
        verbose_name_plural = _('巧购用户月度订单汇总')
        unique_together = ("month", "buyer_id")

    def __unicode__(self):
        return unicode("Month: %s, Buyer: %s." % (self.month, self.buyer_id))
