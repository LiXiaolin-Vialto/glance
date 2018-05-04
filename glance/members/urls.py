from django.conf.urls import url

from . import views

# urls need to be changed later
urlpatterns = [
    url(r'^sub-level-serials/$', views.sub_level_serials),
    url(r'^get-member-orders/$', views.get_member_orders),
    url(r'^get-monthly-data/$', views.get_monthly_data),  # TODO: take date
    # ########################drop later#########################
    url(r'^get-all-orders/$', views.get_all_member_orders),
    url(r'^sub-serials/$', views.sub_serials),
    # ########################drop later#########################
]
