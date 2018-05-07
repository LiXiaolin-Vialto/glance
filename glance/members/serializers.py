# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Serial, Member


class SubLevelSerialSerializer(serializers.Serializer):
    serial = serializers.CharField(required=True)

    class Meta:
        fields = ('serial',)

    def validate(self, data):
        if not Serial.objects.is_exist(data['serial']):
            raise serializers.ValidationError("会员号不存在.")
        return data


class MemberOrdersSerializer(serializers.Serializer):
    serial = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    class Meta:
        fields = ('serial', 'start_date', 'end_date')

    def validate(self, data):
        if not Serial.objects.is_exist(data['serial']):
            raise serializers.ValidationError("会员号不存在.")
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
    mobile = serializers.CharField(required=True)

    class Meta:
        fields = ('from_serial', 'to_serial', 'mobile')

    def validate(self, data):
        from_serial_obj = Serial.objects.get(serial=data['from_serial'])
        # from_serial has to be level0 serial
        if from_serial_obj.level != 0:
            raise serializers.ValidationError(
                "没有权限分配该优宜巧购用户.")

        if not Serial.objects.is_exist(data['to_serial']):
            raise serializers.ValidationError("会员号不存在.")
        to_serial_obj = Serial.objects.get(serial=data['to_serial'])
        # check to_serial is sub serial of from_serial
        if not to_serial_obj.is_subserial_of(from_serial_obj):
            raise serializers.ValidationError(
                "%s 不是 %s 的次级会员." % (to_serial_obj, from_serial_obj))

        # check member mobile exist
        if not Member.objects.is_exist(data['mobile']):
            raise serializers.ValidationError("优宜巧购用户不存在.")
        # member must be managable memeber for from_serial
        member = Member.objects.get(mobile=data['mobile'])
        if member.serial == data['to_serial']:
            raise serializers.ValidationError(
                "优宜巧购用户已经属于该会员.")
        member_pool = from_serial_obj.managed_members()
        if member not in member_pool:
            raise serializers.ValidationError("不能分配此优宜巧购用户.")
        return data


# ########################drop later#########################
# 暂时去全部,稍后学习react之后再使用取日期
class AllMemberOrdersSerializer(serializers.Serializer):
    serial = serializers.CharField(required=True)

    class Meta:
        fields = ('serial',)

    def validate(self, data):
        if not Serial.objects.is_exist(data['serial']):
            raise serializers.ValidationError("会员号不存在.")
        return data
# ########################drop later#########################
