import json

from django.conf import settings
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.urls import path

from menus.menu_builder import update_redis_menus, update_redis_omni_services
from menus.models import ShortCode


def rebuild_menu_cache_support_view(request):
    menus = update_redis_menus()
    omni_services = {
        f'{settings.CACHE_OMNI_KEY_PREFIX}_{settings.COUNTRY_CODE}_{shortcode.shortcode}': update_redis_omni_services(
            shortcode.shortcode) for shortcode in ShortCode.objects.all()}

    menus = [json.dumps(item) for item in menus]
    omni_services = [{item: omni_services[item]} for item in omni_services]
    omni_services = [json.dumps(item) for item in omni_services]
    context = dict(
        admin_site.each_context(request),
        menus=menus,
        omni_services=omni_services)
    return render(request, 'admin/confirm_menu_rebuild.html', context)


# custom admin
class CustomMenuManagerAdmin(AdminSite):
    index_template = 'admin/index_custom.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('rebuild-menu-cache', self.admin_view(rebuild_menu_cache_support_view), name='rebuild_cache'),
        ]
        return my_urls + urls


admin_site = CustomMenuManagerAdmin()
