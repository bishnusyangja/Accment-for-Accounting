from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
                       url(r'^accounts.json$', views.accounts_as_json, name='accounts_as_json'),
                       url(r'^categories.json$', views.categories_as_json, name='accounts_as_json'),
                       url(r'^$', views.list_accounts, name='list_account'),
                       url(r'^detect_category/$', views.detect_category, name='detect_category'),
                       url(r'^create/$', views.account_form, name='create_account'),
                       url(r'^(?P<id>[0-9]+)/update/$', views.account_form, name='update_account'),
                       url(r'^accounts/(?P<day>\d{4}-\d{2}-\d{2}).json$', views.accounts_by_day_as_json,
                           name='accounts_by_day_as_json'),
                       url(r'^accounts.json$', views.accounts_as_json, name='accounts_as_json'),
                       url(r'^(?P<id>[0-9]+)/$', views.view_account, name='view_account'),
                       url(r'^account/(?P<id>[0-9]+)/delete/$', views.delete_account, name='delete_account'),
                       url(r'^search/$', views.search, name='search'),
                       url(r'^ledger-search/$', views.ledger_search, name='ledger_search'),


                       url(r'^parties/$', views.list_all_parties, name='list_all_parties'),
                       url(r'^party/create/$', views.account_form, name='create_party'),
                       url(r'^party/(?P<id>[0-9]+)/$', views.party_form, name='update_party'),
                       url(r'^party/(?P<id>[0-9]+)/delete$', views.delete_party, name='delete_party'),
                       url(r'^party/customers.json$', views.customers_as_json, name='customers_as_json'),
                       url(r'^party/suppliers.json$', views.suppliers_as_json, name='suppliers_as_json'),
                       url(r'^party/vendor/create/$', views.create_vendor_account, name='create_vendor_account'),

                       url(r'^payheads.json$', views.payheads_as_json, name='payheads_as_json'),

                       url(r'^categories/$', views.list_categories, name='list_category'),
                       url(r'^category/create/$', views.create_category, name='create_category'),
                       url(r'^category/details/(?P<id>[0-9]+)/$', views.view_category, name='view_category'),
                       url(r'^category/(?P<id>[0-9]+)/$', views.update_category, name='update_category'),
                       url(r'^category/(?P<id>[0-9]+)/delete$', views.delete_category, name='delete_category'),

                       url(r'^cash-and-vendors.json$', views.cash_and_vendors, name='cash_and_vendors'),
                       url(r'^fixed-assets.json$', views.fixed_assets, name='fixed_assets'),

                       url(r'^cash-book/(?P<id>[0-9]+)$', views.cash_book, name='cash_book'),
                       url(r'^cash-accounts/$', views.list_cash_accounts, name='list_cash_accounts'),

                       url(r'^tax_scheme/create/$', views.tax_scheme, name='create_tax_scheme'),
                       url(r'^tax_scheme/(?P<id>[0-9]+)/$', views.tax_scheme, name='update_tax_scheme'),
                       url(r'^tax_schemes/$', views.list_tax_schemes, name='list_tax_schemes'),
                       url(r'tax-schemes.json', views.tax_schemes_as_json, name='tax_schemes_as_json'),

                       url(r'^interest_scheme/create/$', views.interest_scheme, name='create_interest_scheme'),
                       url(r'^interest_scheme/(?P<id>[0-9]+)/$', views.interest_scheme, name='update_interest_scheme'),
                       url(r'^interest_schemes/$', views.list_interest_schemes, name='list_interest_schemes'),

                       url(r'^create/account-receivables/$', views.account_form, {'category': 'Account Receivables'}, name='create_account_receivables'),
                       url(r'^create/account-payables/$', views.account_form, {'category': 'Account Payables'}, name='create_account_payables'),
                       url(r'^create/purchase/$', views.account_form, {'category': 'Purchase'}, name='create_purchase'),
                       url(r'^create/sales/$', views.account_form, {'category': 'Sales'}, name='create_sales'),
                       url(r'^create/bank-account/$', views.account_form, {'category': 'Bank Account'}, name='create_bank_account'),
                       url(r'^create/cash-account/$', views.account_form, {'category': 'Cash Account'}, name='create_cash_account'),
                       url(r'^create/transfer-remittance/$', views.account_form, {'category': 'Transfer and Remittance'}, name='create_transfer_remittance'),
                       url(r'^create/customer/$', views.account_form, {'category': 'Customers'}, name='create_customer'),
                       url(r'^create/fixed-asset-account/$', views.account_form, {'category': 'Fixed Assets'}, name='create_fixed_asset_account'),
                       url(r'^create/suppliers/$', views.account_form, {'category': 'Suppliers'}, name='create_suppliers'),
                       url(r'^create/account-cash-equivalent/$', views.account_form, {'category': 'Cash Equivalent Account'}, name='create_cash_equivalent'),
                       url(r'^create/account-suppliers/$', views.account_form, {'category': 'Suppliers'}, name='create_suppliers'),
                       url(r'^create/pay-head/$', views.account_form, {'category': 'Pay Head'}, name='create_pay_head'),
                       url(r'^create/employee-deductions/$', views.account_form, {'category': 'Employee Deductions'}, name='create_employee_deductions'),

                       url(r'^create/multiple-account/$', views.multiple_account,  name='create_multiple_account'),
                       url(r'^create/multiple-category/$', views.multiple_category, name='create_multiple_category'),
                       url(r'^save/multiple-account/$', views.save_multiple_account,  name='save_multiple_account'),
                       url(r'^save/multiple-category/$', views.save_multiple_category, name='save_multiple_category'),

)
