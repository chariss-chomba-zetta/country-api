import logging

from menus.menu_builder.menu_screens import *
from menus.settings import LANGUAGE_SUPPORT_SCREENS

_menus_initial_screen = initial_screen  # not used, added to handle menu_screens import
logger = logging.getLogger('CountryApiLogger')


def _build_menu(menu_obj, languages, error_messages):
    try:
        menu_screen_function = eval(menu_obj.menu_type.name)
    except NameError as e:
        raise NameError({f'Screen type: {menu_obj.menu_type.name} has not been found.'}) from e

    if menu_obj.menu_type.name in LANGUAGE_SUPPORT_SCREENS:
        menu = menu_screen_function(menu_obj, languages, error_messages)
    else:
        menu = menu_screen_function(menu_obj)
    return menu
