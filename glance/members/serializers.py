# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Serial, Member


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


class AssginMemberSerializer(serializers.Serializer):
    # 分配member的serial
    from_serial = serializers.CharField(required=True)
    to_serial = serializers.CharField(required=True)
    moblie = serializers.CharField(required=True)

    class Meta:
        fields = ('from_serial', 'to_serial', 'moblie')

    def validate(self, data):
        from_serial_obj = Serial.objects.get(data['from_serial'])
        # from_serial has to be level0 serial
        if from_serial_obj.level != 0:
            raise serializers.ValidationError(
                "Serial does not have the privilege to assign members.")

        if not Serial.objects.is_exist(data['to_serial']):
            raise serializers.ValidationError("Serial does not exist.")
        to_serial_obj = Serial.objects.get(data['to_serial'])
        # check to_serial is sub serial of from_serial
        if not to_serial_obj.is_subserial_of(from_serial_obj):
            raise serializers.ValidationError(
                "%s is not subserial of %s." % (to_serial_obj,
                                                from_serial_obj))

        # check member mobile exist
        if not Member.objects.is_exist(data['moblie']):
            raise serializers.ValidationError("Member does not exist.")
        # member must be managable memeber for from_serial
        member = Member.objects.get(moblie=data['moblie'])
        member_pool = from_serial_obj.managed_members()
        if member not in member_pool:
            raise serializers.ValidationError("Can not assign this member.")
        return data


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
