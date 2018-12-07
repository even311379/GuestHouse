# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['news', 'about', 'roomtype','booking','calendar_widget','message_area']

    def location(self, item):
        return reverse(item)
