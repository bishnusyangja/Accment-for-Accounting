from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',


                       url(r'^journals/$', views.list_journal_vouchers, name='list_journal_vouchers'),
                       url(r'^journal/$', views.journal_voucher, name='new_journal_voucher'),
                       url(r'^journal/(?P<id>[0-9]+)/$', views.journal_voucher, name='update_journal_voucher'),
                       url(r'^journal/save/$', views.save_journal_voucher, name='save_journal_voucher'),
                       url(r'^journal/approve/$', views.approve_journal_voucher, name='approve_journal_voucher'),
                       url(r'^journal/cancel/$', views.cancel_journal_voucher, name='cancel_journal_voucher'),
                       url(r'^journals/search/$', views.journals_search, name='journals_search'),
                       url(r'^journal/unapprove/(?P<id>[0-9]+)/$', views.unapprove_journal_voucher,
                           name='unapprove_journal_voucher'),
                       url(r'^journal/(?P<id>[0-9]+)/delete/$', views.delete_journal_voucher,
                           name='delete_journal_voucher'),
                       url(r'^journal/attachment/delete/(?P<id>[0-9]+)/$', views.delete_journal_attachment,
                           name='delete_journal_voucher_attachment'),

                       url(r'^purchase-voucher/$', views.purchase_voucher, name='new_purchase_voucher'),
                       url(r'^purchase-voucher/(?P<id>[0-9]+)/$', views.purchase_voucher, name='update_purchase_voucher'),
                       url(r'^purchase-voucher/save/$', views.save_purchase_voucher, name='save_purchase_voucher'),
                       url(r'^purchase-voucher/delete/(?P<id>[0-9]+)/$', views.delete_purchase_voucher, name='delete_purchase_voucher'),
                       url(r'^purchase-voucher/attachment/delete/(?P<id>[0-9]+)/$', views.delete_purchase_voucher_attachment, name='delete_purchase_voucher_attachment'),
                       url(r'^purchase-vouchers/$', views.list_purchase_vouchers, name='list_purchase_vouchers'),
                       url(r'^purchase-vouchers/search/$', views.search_purchase_vouchers, name='search_purchase_vouchers'),
                       url(r'^purchase-voucher/approve/$', views.approve_purchase_voucher, name='approve_purchase_voucher'),
                       url(r'^purchase-voucher/unapprove/(?P<id>[0-9]+)/$', views.unapprove_purchase_voucher, name='unapprove_purchase_voucher'),

                       url(r'^invoices/$', views.all_invoices, name='all_invoices'),
                       url(r'^invoices/search/$', views.all_invoices_search, name='all_invoices_search'),
                       url(r'^invoice/$', views.invoice, name='new_invoice'),
                       url(r'^invoice/(?P<id>[0-9]+)/$', views.invoice, name='view_invoice'),
                       url(r'^invoice/party/(?P<id>[0-9]+).json$', views.party_invoices, name='party_invoices'),
                       url(r'^invoice/(?P<id>[0-9]+)/delete/$', views.delete_invoice, name='delete_invoice'),
                       url(r'^invoice/save/$', views.save_invoice, name='save_invoice'),
                       url(r'^invoice/approve/$', views.approve_invoice, name='approve_invoice'),
                       url(r'^invoice/unapprove/(?P<id>[0-9]+)/$', views.unapprove_invoice, name='unapprove_invoice'),
                       url(r'^invoice/cancel/$', views.cancel_invoice, name='cancel_invoice'),

                       url(r'^cash-receipts/$', views.list_cash_receipts, name='list_cash_receipts'),
                       url(r'^cash-receipts/search/$', views.cash_receipts_search, name='cash_receipts_search'),

                       url(r'^cash-receipt/$', views.cash_receipt, name='create_cash_receipt'),
                       url(r'^cash-receipt/(?P<id>[0-9]+)/$', views.cash_receipt, name='update_cash_receipt'),
                       # url(r'^cash-receipt/save/$', views.save_cash_receipt, name='save_cash_receipt'),
                       url(r'^cash-receipt/delete/(?P<id>[0-9]+)/$', views.delete_cash_receipt, name='delete_cash_receipt'),
                       url(r'^cash-receipt/deleted/(?P<id>[0-9]+)/$', views.deleted_cash_receipt, name='deleted_cash_receipt'),
                       url(r'^cash-receipt/approve/$', views.approve_cash_receipt, name='approve_cash_receipt'),
                       url(r'^cash-receipt/save/$', views.save_cash_receipt, name='save_cash_receipt'),
                       url(r'^cash-receipt/unapprove/(?P<id>[0-9]+)/$', views.unapprove_cash_receipt,
                           name='unapprove_cash_receipt'),

                       url(r'^cash-payments/$', views.list_cash_payments, name='list_cash_payments'),
                       url(r'^cash-payments/search/$', views.cash_payments_search, name='cash_payments_search'),

                       url(r'^cash-payment/$', views.cash_payment, name='create_cash_payment'),
                       url(r'^cash-payment/(?P<id>[0-9]+)/$', views.cash_payment, name='update_cash_payment'),
                       # url(r'^cash-payment/save/$', views.save_cash_payment, name='save_cash_payment'),
                        url(r'^cash-payment/delete/(?P<id>[0-9]+)$', views.delete_cash_payment, name='delete_cash_payment'),
                        url(r'^cash-payment/deleted/(?P<id>[0-9]+)$', views.deleted_cash_payment, name='deleted_cash_payment'),
                       url(r'^cash-payment/approve/$', views.approve_cash_payment, name='approve_cash_payment'),
                       url(r'^cash-payment/save/$', views.save_cash_payment, name='save_cash_payment'),
                       url(r'^cash-payment/unapprove/(?P<id>[0-9]+)/$', views.unapprove_cash_payment,
                           name='unapprove_cash_payment'),

                       url(r'^fixed-assets/$', views.list_fixed_assets, name='list_fixed_assets'),
                       url(r'^fixed-asset/$', views.fixed_asset, name='create_fixed_asset'),
                       url(r'^fixed-asset/(?P<id>[0-9]+)/$', views.fixed_asset, name='update_fixed_asset'),
                       url(r'^fixed-asset/save/$', views.save_fixed_asset, name='save_fixed_asset'),
                       url(r'^fixed-asset/approve/$', views.approve_fixed_asset, name='approve_fixed_asset'),
                       url(r'^fixed-asset/unapprove/$', views.unapprove_fixed_asset, name='unapprove_fixed_asset'),
                       url(r'^fixed-asset/delete/(?P<id>[0-9]+)/$', views.delete_fixed_asset, name='delete_fixed_asset'),
                       url(r'^all-unapproved-vouchers/$', views.all_unapproved_vouchers, name='all_unapproved_vouchers'),

)
