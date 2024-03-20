import datetime
import logging

from menus.menu_builder.exceptions import MenuGenerationException
from menus.menu_builder.menu_builder import _build_menu
from menus.menu_builder.tools import get_error_messages, get_menu_key
from menus.models import Language, ShortCode, UssdMenu
from menus.settings import INITIAL_SCREEN_NAME

logger = logging.getLogger('CountryApiLogger')


def _build_menus(shortcode=None):
    menus = {}
    qs = UssdMenu.objects.all()
    if shortcode is not None:
        qs = qs.filter(shortcode__shortcode=shortcode)
        logger.debug(f'UssdMenu Queryset count:{qs.count()}')
    languages = list(Language.objects.all())
    error_messages = get_error_messages(languages)
    # check initial screens - only one per screen is allowed
    all_shortcodes = ShortCode.objects.get_full_queryset()
    for shortcode_obj in all_shortcodes:
        count = UssdMenu.objects.get_full_queryset().filter(
            shortcode=shortcode_obj, menu_type__name=INITIAL_SCREEN_NAME).count()
        if count > 1:
            error_message = f'Two or more {INITIAL_SCREEN_NAME} found for shortcode: {shortcode_obj}. One is allowed.'
            raise MenuGenerationException(error_message=error_message)
        # if initial screen exists, add custom error quit screen as well, if not added already
        quit_screen_name = UssdMenu.generate_custom_error_screen_name(shortcode_obj=shortcode_obj)
        if count == 1 and not UssdMenu.objects.filter(name__exact=quit_screen_name).exists():
            UssdMenu.create_custom_quit_screen(shortcode_obj=shortcode_obj)

    for menu_obj in qs:
        start_time = datetime.datetime.now()

        menu_key = get_menu_key(shortcode=menu_obj.shortcode.shortcode)
        if menu_key not in menus:
            menus[menu_key] = {}

        menu_name = menu_obj.name
        if menu_obj.menu_type.name == 'initial_screen':
            menu_name = 'initial_screen'

        menus[menu_key][menu_name] = _build_menu(menu_obj=menu_obj, languages=languages, error_messages=error_messages)

        runtime = int((datetime.datetime.now() - start_time).microseconds / 1000)
        logger.info('-------------menu: %s, id: %s, type: %s, time: %s', str(menu_obj), str(menu_obj.pk),
                    str(menu_obj.menu_type.name), str(runtime))

    return menus
