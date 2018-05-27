# -*- coding: utf-8 -*-
import logging
import time

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from django.db import connections
from django.db import transaction
from django.db.models import Sum

from members.models import Member, Order, MonthlyData


logger = logging.getLogger(__name__)

# =============================================
ALL_MEMBER_SQL = """
SELECT
    user_id,user_name,email,phone_mob,reg_time
FROM
    ecmall.ecm_member
where phone_mob is not null;
"""

ALL_ORDERS_SQL = """
SELECT
    order_sn,buyer_id,buyer_name,goods_amount,add_time,finished_time
FROM
    ecmall.ecm_order
WHERE
    status = 40;
"""
# =============================================


def timestamp_converter(timestamp):
    """将时间戳转换成datetime"""
    time_str = time.strftime("%b %d %Y %I:%M%p", time.localtime(timestamp))
    dt_obj = datetime.strptime(time_str, '%b %d %Y %I:%M%p')
    return dt_obj


def get_data_from_external(sql):
    """获取外部数据库的数据"""
    cursor = connections['external'].cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


@transaction.atomic
def create_members():
    rows = get_data_from_external(ALL_MEMBER_SQL)
    if rows:
        for row in rows:
            member = Member.objects.create(name=row[1],
                                           email=row[2],
                                           mobile=row[3],
                                           uid=str(row[0]),
                                           reg_time=timestamp_converter(row[4]))
            print member


@transaction.atomic
def create_orders():
    rows = get_data_from_external(ALL_ORDERS_SQL)
    if rows:
        for row in rows:
            order = Order.objects.create(order_number=str(row[0]),
                                         buyer_id=str(row[1]),
                                         buyer_name=row[2],
                                         total=row[3],
                                         order_time=timestamp_converter(row[4]),
                                         finished_time=timestamp_converter(row[5]))
            print order


@transaction.atomic
def create_monthly_data():
    result = []
    # 下次运行, 需要修改,
    today = date.today()
    current = date(2015, 10, 1)

    while current <= today:
        result.append(current)
        current += relativedelta(months=1)

    for d in result:
        YESTERDAY = d - timedelta(1)
        print "get %s montly data." % YESTERDAY
        last_month_orders = Order.objects.filter(
            finished_time__year=YESTERDAY.year,
            finished_time__month=YESTERDAY.month)

        for d in last_month_orders.values('buyer_id').distinct():
            orders = last_month_orders.filter(
                buyer_id=d['buyer_id'])
            MonthlyData.objects.create(month=YESTERDAY.strftime("%Y-%m"),
                                       buyer_id=d['buyer_id'],
                                       buyer_name=orders[0].buyer_name,
                                       total=orders.aggregate(
                                           Sum('total'))["total__sum"],
                                       amount=len(orders))


create_members()
create_orders()
create_monthly_data()
