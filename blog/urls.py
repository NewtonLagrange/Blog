from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

app_name = 'blog'
urlpatterns = [

    url(r'^favicon\.ico$', RedirectView.as_view(url=r'/static/img/favicon.ico')),
    url(r'^detail/(\d+)/$', views.detail, name='detail'),
    url(r'^category/(\d+)/$', views.category, name='category'),
    url(r'^tag/(\d+)/$', views.tag, name='tag'),
    url(r'^date/(.*?)/$', views.date, name='date'),
    url(r'^write/$', views.write, name='write'),
    url(r'^feed/$', views.RSSFeed(), name="RSS"),
]
