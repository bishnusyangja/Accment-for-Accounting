from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^settings/$', views.bank_settings, name='bank_settings'),

                       url(r'^bank-deposits/$', views.list_bank_deposits, name='list_bank_deposits'),
                       url(r'^bank-deposits/search/$', views.bank_deposits_search, name='bank_deposits_search'),

                       url(r'^bank-deposit/$', views.bank_deposit, name='bank_deposit'),
                       url(r'^bank-deposit/update/(?P<id>[0-9]+)$', views.bank_deposit, name='update_bank_deposit'),
                       url(r'^bank-deposit/approve/$', views.approve_bank_deposit, name='approve_bank_deposit'),
                       url(r'^bank-deposit/save/$', views.save_bank_deposit, name='save_bank_deposit'),
                       url(r'^bank-deposit/delete/(?P<id>[0-9]+)$', views.delete_bank_deposit,
                           name='delete_bank_deposit'),
                       url(r'^bank-deposit/delete-attachment/(?P<id>[0-9]+)$', views.delete_bank_deposit_attachment,
                           name='delete_bank_deposit_attachment'),
                       url(r'^bank-deposit/deleted/(?P<id>[0-9]+)$', views.deleted_bank_deposit,
                           name='deleted_bank_deposit'),
                       url(r'^bank-deposit/unapprove/(?P<id>[0-9]+)$', views.unapprove_bank_deposit,
                           name='unapprove_bank_deposit'),

                       url(r'^bank-payments/$', views.list_bank_payments, name='list_bank_payments'),
                       url(r'^bank-payments/search/$', views.bank_payments_search, name='bank_payments_search'),

                       url(r'^bank-payment/$', views.bank_payment, name='bank_payment'),
                       url(r'^bank-payment/save/$', views.save_bank_payment, name='save_bank_payment'),
                       url(r'^bank-payment/update/(?P<id>[0-9]+)$', views.bank_payment, name='update_bank_payment'),
                       url(r'^bank-payment/approve/$', views.approve_bank_payment, name='approve_bank_payment'),
                       url(r'^bank-payment/delete/(?P<id>[0-9]+)$', views.delete_bank_payment,
                           name='delete_bank_payment'),
                       url(r'^bank-payment/deleted/(?P<id>[0-9]+)$', views.deleted_bank_payment,
                           name='deleted_bank_payment'),
                       url(r'^bank-payment/unapprove/(?P<id>[0-9]+)$', views.unapprove_bank_payment,
                           name='unapprove_bank_payment'),

                       url(r'^accounts/$', views.list_bank_accounts, name='list_bank_accounts'),
                       url(r'^book/(?P<id>[0-9]+)$', views.bank_book, name='bank_book'),
)

