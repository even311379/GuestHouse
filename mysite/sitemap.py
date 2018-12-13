# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from django.utils import timezone

class StaticViewSitemap(sitemaps.Sitemap):

    changefreq = 'weekly'
    
    def items(self):
        return ['news', 'about', 'roomtype','booking','calendar_widget','message_area']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()
