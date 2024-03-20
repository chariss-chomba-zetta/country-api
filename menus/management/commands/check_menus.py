import logging

from django.core.management.base import BaseCommand

from menus.menu_builder import build_menus
from menus.menu_builder.tools import check_model_for_zombie_objects
from menus.models import MenuItem, MenuOption, RouterOption, UssdLabel

logger = logging.getLogger('CountryApiLogger')


class Command(BaseCommand):
    help = 'Perform menu objects sanity checks'

    def handle(self, *args, **options):
        build_menus()
        for obj in [MenuItem, MenuOption, RouterOption, UssdLabel]:
            for qs in check_model_for_zombie_objects(obj):
                if qs.exists() != 0:
                    item_pks = ','.join([single_item.pk for single_item in qs])
                    self.stdout.write(self.style.ERROR(
                        f'Found zombie objects for: {obj._meta.object_name}\n'
                        f'Queryset is: {qs}\n'
                        f'PKs: {item_pks}'),
                    )
                else:
                    self.stdout.write(self.style.SUCCESS(f'NO zombie objects for: {obj._meta.object_name}\n'))
