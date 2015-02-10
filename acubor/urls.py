from django.conf.urls import patterns, url, include
from core import views as core_views
from users import views as users_views
from django.conf import settings

# from django.views.generic import TemplateView
from rest_framework import viewsets, routers
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib import admin
from views import error_404
admin.autodiscover()


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = get_user_model()

# class GroupViewSet(viewsets.ModelViewSet):
#     model = Group

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = patterns('',

                       url(r'^application/', users_views.index, name='home'),
                       url(r'^$', users_views.home_page, name='home_page'),
                       url(r'^about-us/$', users_views.about_us, name='about_us_page'),
                       url(r'^product-features/$', users_views.product_features, name='features_page'),
                       (r'^user/', include('users.urls')),
                       (r'^voucher/', include('voucher.urls')),
                       (r'^tax/', include('tax.urls')),
                       (r'^inventory/', include('inventory.urls')),
                       (r'^day/', include('dayjournal.urls')),
                       (r'^ledger/', include('ledger.urls')),
                       (r'^payroll/', include('payroll.urls')),
                       (r'^bank/', include('bank.urls')),
                       (r'^report/', include('report.urls')),
                       (r'^blog/', include('blog.urls')),
                       # (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
                       url(r'^settings/company/$', core_views.company_settings, name='company_settings'),
                       url(r'^settings/user/$', users_views.user_setting, name='user_settings'),
                       url(r'^settings/voucher/$', core_views.voucher_settings, name='voucher_settings'),

                       url(r'^redactor/', include('redactor.urls')),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^', include(router.urls)),
                       url(r'^acubor-admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^acubor-admin/', include(admin.site.urls)),
                       # url(r'^not-found/$', error_404),
)


if not settings.ON_OPENSHIFT:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^user_uploads/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
