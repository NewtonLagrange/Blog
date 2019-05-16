from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

app_name = 'Index'
urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),
    url(r'^$', views.index, name='index'),

]
