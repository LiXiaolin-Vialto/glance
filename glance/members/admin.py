# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Serial, Member


# class MemberInline(admin.StackedInline):
#     model = Member


@admin.register(Serial)
class SerialAdmin(admin.ModelAdmin):
    list_display = ('serial', 'level', 'name', 'moblie')
    readonly_fields = ('level', 'number_of_members')
    # inlines = [
    #     MemberInline,
    # ]

    def number_of_members(self, obj):
        return len(Member.objects.filter(serial=obj.serial))
