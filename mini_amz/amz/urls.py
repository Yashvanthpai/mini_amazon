from django.conf.urls import url
from amz import views
from django.contrib.auth.views import LoginView
from django.contrib.sessions.models import Session

urlpatterns = [
    url(r'logout/$',views.logingout,name='logout'),
    url(r'login/$',LoginView.as_view(template_name="LoginView.html",extra_context={'about':'yes','register':'','contact':'yes'}),name="login"),
    url(r'register/$',views.registration,name="register"),
    url(r'about/$',views.about,name='one'),
    url(r'conatact/$',views.contact,name='two'),
    url(r'logedin/$',views.logedin,name='logedin'),
    url(r'inventory/$',views.inventory,name='inventory'),
    url(r'cart/$',views.cart,name='cart'),
    url(r'^$',views.index,name='index'),
]