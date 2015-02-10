from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
                       url(r'^schemes/$', views.list_tax_schemes, name='list_tax_schemes'),
                       url(r'^scheme/create/$', views.tax_scheme_form, name='create_tax_scheme'),
                       url(r'^scheme/(?P<id>[0-9]+)/$', views.tax_scheme_form, name='update_tax_scheme'),
                       url(r'^schemes/json/$', views.schemes_as_json, name='tax_schemes_as_json'),
                       url(r'^scheme/delete/(?P<id>[0-9]+)/$', views.delete_tax_scheme, name='delete_tax_scheme'),
)

