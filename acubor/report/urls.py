# url for the report
from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
                       url(r'^trial-balance/$', views.trial_balance, name='trial_balance'),
                       url(r'^trial-balance/(?P<count>\d+)/$', views.trial_balance, name='trial_bal'),
                       url(r'^profit-and-loss/$', views.profit_and_loss, name='profit_and_loss'),
                       url(r'^profit-and-loss/(?P<end_date1>\d{2}-\d{2}-\d{4})/$', views.profit_and_loss, name='profit_and_loss_by_date'),
                       url(r'^balance-sheet/$', views.balance_sheet, name='balance_sheet'),
)
