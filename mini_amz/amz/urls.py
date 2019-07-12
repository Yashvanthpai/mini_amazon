from django.conf.urls import url
from amz import views
urlpatterns = [
    url(r'about/$',views.one,name='one'),
    url(r'^',views.index,name='index'),
]