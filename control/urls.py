from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send_command/$', views.run_code, name='run_code'),
    url(r'^live_data/$', views.live_data, name='live_data'),
    url(r'^live_data/api$', views.AttitudeGraphApiView.as_view(), name='live_data_api'),
]
