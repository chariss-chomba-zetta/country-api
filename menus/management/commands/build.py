import logging

from django.core.management.base import BaseCommand

from menus.menu_builder import update_redis_menus, update_redis_omni_services
from menus.models import ShortCode

logger = logging.getLogger('CountryApiLogger')


class Command(BaseCommand):
    help = 'Build menu all items and update cache'

    def handle(self, *args, **options):
        shortcodes = ShortCode.objects.all()
        for shortcode in shortcodes:
            update_redis_menus(shortcode=shortcode)
            self.stdout.write(self.style.SUCCESS(f'Menus have been built and updated successfully for {shortcode}.'))

            update_redis_omni_services(shortcode=shortcode)
            self.stdout.write(
                self.style.SUCCESS(f'OMNI services have been built and updated successfully for {shortcode}.'))
