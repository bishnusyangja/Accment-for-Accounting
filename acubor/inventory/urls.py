from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',

                       url(r'^physicalstocks/$', views.all_physical_stocks, name='all_physical_stocks'),
                       url(r'^physicalstock/$', views.physical_stock, name='new_physical_stock'),
                       url(r'^physicalstock/(?P<id>[0-9]+)/$', views.physical_stock, name='view_physical_stock'),
                       url(r'^physicalstock/delete/(?P<voucher_no>[0-9]+)/$', views.delete_physical_stock,
                           name='delete_physical_stock'),
                       url(r'^physicalstock/unapprove/(?P<id>[0-9]+)/$', views.unapprove_physical_stock,
                           name='unapprove_physical_stock'),
                       url(r'^physicalstock/save/$', views.save_physical_stock, name='save_physical_stock'),
                       url(r'^physicalstock/approve/$', views.approve_physical_stock, name='approve_physical_stock'),
                       url(r'^physicalstock/cancel/$', views.cancel_physical_stock, name='cancel_physical_stock'),

                       url(r'^items/$', views.list_all_items, name='list_all_items'),
                       url(r'^create/$', views.item_form, name='create_inventory_item'),
                       url(r'^item/delete/(?P<id>[0-9]+)$', views.delete_inventory_item, name='delete_inventory_item'),
                       url(r'^create_item/$', views.create_item, name='create_inventory_item_returning_item_no_fuel'),
                       url(r'^create_item/(?P<id>[0-9]+)/$', views.create_item,
                           name='create_inventory_item_returning_item'),

                       url(r'^items/json/$', views.items_as_json, name='items_as_json'),
                       url(r'^accounts.json$', views.accounts_as_json, name='accounts_as_json'),
                       url(r'^accounts/(?P<day>\d{4}-\d{2}-\d{2}).json$', views.accounts_by_day_as_json,
                           name='accounts_by_day_as_json'),
                       url(r'^items/(?P<day>\d{4}-\d{2}-\d{2}).json$', views.items_by_day_as_json,
                           name='items_by_day_as_json'),
                       url(r'^(?P<id>[0-9]+)/$', views.item_form, name='update_inventory_item'),

                       url(r'^categories/$', views.list_categories, name='list_inventory_category'),
                       url(r'^category/create/$', views.create_category, name='create_inventory_category'),
                       url(r'^category/(?P<id>[0-9]+)/$', views.update_category, name='update_inventory_category'),
                       url(r'^category/(?P<id>[0-9]+)/delete$', views.delete_category,
                           name='delete_inventory_category'),

                       url(r'^units/$', views.list_units, name='list_units'),
                       url(r'^unit/create/$', views.unit_form, name='create_unit'),
                       url(r'^unit/(?P<id>[0-9]+)/$', views.unit_form, name='update_unit'),
                       url(r'^unit/(?P<id>[0-9]+)/delete$', views.delete_unit, name='delete_unit'),

                       url(r'^stock-ledger/(?P<id>[0-9]+)/$', views.view_stock_ledger, name='view_stock_ledger'),
)

