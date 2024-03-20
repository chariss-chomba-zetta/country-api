from django.conf import settings
from django.db.models import ForeignKey

from menus.menu_builder.settings import FORBIDDEN_SESSION_KEYS
from menus.models import ErrorLabel
from menus.settings import ERROR_MESSAGE_TEXT_FALLBACK


def get_menu_key(shortcode):
    key = f'{settings.CACHE_MENU_KEY_PREFIX}_{settings.COUNTRY_CODE}_{shortcode}'
    return key


def initialize_dict_response(menu_obj) -> dict:
    menu_screen_specs = {'type': menu_obj.menu_type.name}
    return menu_screen_specs


def get_error_messages(languages):
    error_messages = {}
    for language in languages:
        try:
            error_message = ErrorLabel.objects.get(language=language).error_message
        except ErrorLabel.DoesNotExist:
            error_message = ERROR_MESSAGE_TEXT_FALLBACK
        error_messages[language.language_code] = error_message
    return error_messages


def check_session_key_in_forbidden_list(session_key):
    """
    Checks the provided session key against session keys that are used by the USSD FRAMEWORK.
    Returns True if session_key is okay.
    """
    return session_key in FORBIDDEN_SESSION_KEYS


def check_model_for_zombie_objects(model, delete_objects=False):
    fk_fields = [item.name for item in model._meta.fields if
                 isinstance(item, ForeignKey) and item.related_model._meta.object_name == 'UssdMenu']
    filters = [{f'{field}__isnull': True} for field in fk_fields]
    result_qs_list = [model.objects.filter(**item) for item in filters]
    return result_qs_list
