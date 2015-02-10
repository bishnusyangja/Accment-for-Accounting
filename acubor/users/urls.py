from django.conf.urls import patterns, include, url
from registration.backends.default.views import RegistrationView
from rest_framework.urlpatterns import format_suffix_patterns

from users.forms import UserRegistrationForm
from users import views
from users.views import UserList


urlpatterns = patterns('',
                       url(r'^login/$', views.web_login, {'template_name': 'registration/login.html'},
                           name='auth_login'),
                       url(r'^register/$', RegistrationView.as_view(form_class=UserRegistrationForm,
                                                                    template_name='registration/registration_form.html')),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^list-attachments/$', views.list_user_attachments, name='list_user_attachments'),
                       url(r'^attachment/process/$', views.attachment_process, name='attachment_process'),
                       url(r'^request-new-user/$', views.request_new_user, name='request_new_user'),
                       # url(r'^generate-password/$', views.generate_password, name='generate_password'),

                       url(r'^set-company/(?P<id>[0-9]+)/$', views.set_company, name='set_company'),

                       url(r'^roles/$', views.roles, name='roles'),
                       url(r'^user_attachments/$', views.user_attachments, name='user_attachments'),
                       url(r'^save_user_attachments/$', views.save_user_attachments, name='save_user_attachments'),
                       url(r'^delete_user_attachments/$', views.delete_user_attachments,
                           name='delete_user_attachments'),
                       url(r'^role/delete/(?P<id>[0-9]+)/$', views.delete_role, name='delete_role'),


                       url(r'^list$', UserList.as_view(), name='user-list'),
                       # url(r'^$', 'users.views.profile'),
                       # url(r'^edit/$', 'users.views.edit_profile'),
                       # url(r'^auth-error/$', 'users.views.auth_error'),
                       (r'^', include('registration.backends.default.urls')),
                       # url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$', 'users.views.profile', name='user-detail'),
                       url(r'^save-time/$', views.save_time, name='save_time'),
                       url(r'^sales-pie-chart/$', views.sales_pie_chart, name='sales_pie_chart'),
                       url(r'^sales-line-chart/$', views.sales_line_chart, name='sales_line_chart'),
                       url(r'^income-expense-chart/$', views.income_expense_chart, name='income_expense_chart'),
                       url(r'^company/setup/$', views.company_setup, name='company_setup'),
                       url(r'get-ip-infos/$', views.get_ip_infos, name="get_ip_infos"),
                       url(r'subscription/status/$', views.subscription_status, name="subscription_status")
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
