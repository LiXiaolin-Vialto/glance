# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Serial, Member


@admin.register(Serial)
class SerialAdmin(admin.ModelAdmin):
    list_display = ('serial', 'level', 'name', 'mobile')
    readonly_fields = ('is_supper', 'mobile', 'name', 'user',
                       'level', 'number_of_members')

    def number_of_members(self, obj):
        return len(Member.objects.filter(serial=obj.serial))
    number_of_members.short_description = '优宜巧购用户数'

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'serial',
                    'serial_changed', 'serial_history',
                    'uid', 'reg_time')
    readonly_fields = ('name', 'mobile', 'email',
                       'serial_changed', 'serial_history',
                       'uid', 'reg_time')

    def has_delete_permission(self, request, obj=None):
        return False
