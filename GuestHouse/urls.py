"""GuestHouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps import views as sv
from mysite import views , sitemap


sitemaps_ = {
    'static': sitemap.StaticViewSitemap,
}


app_name = 'mysite'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('news', views.news, name='news'),
    path('about', views.about, name='about'),
    path('roomtype', views.roomtype, name='roomtype'),
    path('booking', views.booking, name='booking'),
    path('ajax/booking_validate_date/', views.booking_validate_date, name='booking_validate_date'),
    path('traffic', views.traffic, name='traffic_info'),
    path('nearby', views.nearby, name='nearby'),
    path('booking_check', views.booking_check, name='booking_check'),
    path('add_booking_data', views.add_booking_data, name='add_booking_data'),
    path('booking_data_confirm/', views.booking_data_confirm,
         name='booking_data_confirm'),
    path('booking_success', views.booking_success),
    path('booking_fail', views.booking_fail),
    path('calendar', views.calendar_widget, name='calendar_widget'),
    path('message_area', views.message_area, name='message_area'),
    path('add_message', views.add_message, name='add_message'),
    path('test',views.test, name='test'),
    path('sitemap.xml', sv.sitemap, {'sitemaps': sitemaps_},name='django.contrib.sitemaps.views.sitemap'),
     ]

urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL,
#                         document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})]
