# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Serial


class SubLevelSerialSerializer(serializers.Serializer):
    serial = serializers.CharField(required=True)

    class Meta:
        fields = ('serial',)

    def validate(self, data):
        if not Serial.objects.is_exist(data['serial']):
            raise serializers.ValidationError("Serial does not exist.")
        return data


class MemberOrdersSerializer(serializers.Serializer):
    serial = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    class Meta:
        fields = ('serial', 'start_date', 'end_date')

    def validate(self, data):
        if not Serial.objects.is_exist(data['serial']):
            raise serializers.ValidationError("Serial does not exist.")
        return data
    # todo validate date
    # def validate(self, data):
    #     if query_start_date >= query_end_date:
    #         raise ...
    #     return data


# ########################drop later#########################
# 暂时去全部,稍后学习react之后再使用取日期
class AllMemberOrdersSerializer(serializers.Serializer):
    serial = serializers.CharField(required=True)

    class Meta:
        fields = ('serial',)

    def validate(self, data):
        if not Serial.objects.is_exist(data['serial']):
            raise serializers.ValidationError("Serial does not exist.")
        return data
# ########################drop later#########################
