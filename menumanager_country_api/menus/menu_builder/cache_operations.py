import logging
import traceback
from django.conf import settings

from base_app.cache_tools import BASE_CACHE, db_move_redis_key, get_object_from_cache, remove_cache_key, \
    TEMP_CACHE, update_cache_key
from menumanager_country_api.settings.base import CACHE_MENU_KEY_PREFIX, COUNTRY_CODE
from menus.menu_builder import build_menus
from menus.models import ShortCode, UssdMenu
from menus.settings import FUNCTION_SCREEN_NAME

logger = logging.getLogger('CountryApiLogger')


def _update_redis_menus(shortcode=None):
    """
    Use this function to generate menus for all shortcodes in db=15 and transfer menus to the db=0/default/
    """

    if shortcode is not None:
        shortcodes = [shortcode]
    else:
        shortcodes = [item.shortcode for item in ShortCode.objects.all()]
    logger.debug(f"Redis connection Details:Host:{settings.REDIS_HOST}" +
                 f"|Port:{settings.REDIS_PORT}|SSL:{settings.REDIS_SSL}|CERT:{settings.REDIS_SSL_CERT}")
    try:
        menu_keys = []
        logger.debug('=============Starting to Build Menus===================')
        for short_code in shortcodes:
            menu_key = f'{CACHE_MENU_KEY_PREFIX}_{COUNTRY_CODE}_{short_code}'
            logger.info(f'=============Menu Key:{menu_key}====================')
            menu_keys.append(menu_key)
            temp_menu = build_menus(shortcode=short_code)
            remove_cache_key(TEMP_CACHE, menu_key)
            logger.info('===========Finished removing cache keys==============')
            update_cache_key(cache=TEMP_CACHE, key=menu_key, value=temp_menu)
            logger.info('===========Updated cache key==================')
            db_move_redis_key(source_cache=TEMP_CACHE, target_cache=BASE_CACHE, key=menu_key)
            logger.info('============Successfully switched redis DB =====================')
        menus = [get_object_from_cache(cache=BASE_CACHE, key=item) for item in menu_keys]
    except Exception as e:
        log_msg = f'_update_redis_menus|Error is:{traceback.format_exc()}'
        logger.error(log_msg)
        return log_msg
    logger.debug(f'===========Hurreh finally we have menus:============================')
    return menus


def _update_redis_omni_services(shortcode):
    """
    Use this function to get omni services for all menus and update REDIS
    """
    omni_services = {}
    try:
        logger.debug('=============Starting to Build Omni Services ===================')
        logger.debug(f"Redis connection Details:Host:{settings.REDIS_HOST}" +
                     f"|Port:{settings.REDIS_PORT}|SSL:{settings.REDIS_SSL}|CERT:{settings.REDIS_SSL_CERT}")
        qs = UssdMenu.objects.filter(shortcode__shortcode=shortcode, menu_type__name=FUNCTION_SCREEN_NAME)
        for menu_obj in qs:
            service_name_key = menu_obj.omni_service.name
            degradation_key = menu_obj.omni_service.service_degradation_key
            # logger.debug(f"{menu_obj.omni_service.name}|{menu_obj.omni_service.service_function}|"+
            #     f"{menu_obj.omni_service.url}|{menu_obj.omni_service.method}|{menu_obj.omni_service.session_key}")
            if service_name_key not in omni_services:
                omni_services[service_name_key] = {}
            omni_services[service_name_key]['name'] = menu_obj.omni_service.name
            omni_services[service_name_key]['service_function'] = menu_obj.omni_service.service_function
            omni_services[service_name_key]['url'] = menu_obj.omni_service.url
            omni_services[service_name_key]['method'] = menu_obj.omni_service.method
            omni_services[service_name_key]['session_key'] = menu_obj.omni_service.session_key
            omni_services[service_name_key]['service_degradation_key'] = degradation_key if bool(
                degradation_key) else None

        omni_service_key = f'{settings.CACHE_OMNI_KEY_PREFIX}_{settings.COUNTRY_CODE}_{shortcode}'

        remove_cache_key(TEMP_CACHE, omni_service_key)
        logger.info('===========Finished removing omni service cache keys==============')
        update_cache_key(cache=TEMP_CACHE, key=omni_service_key, value=omni_services)
        logger.info('===========Updated omni service cache key==================')
        db_move_redis_key(source_cache=TEMP_CACHE, target_cache=BASE_CACHE, key=omni_service_key)
        logger.info('============Successfully switched redis omni service DB =====================')
        omni_services = get_object_from_cache(cache=BASE_CACHE, key=omni_service_key)
    except Exception:
        log_msg = f'_update_redis_omni_services|Error is:{traceback.format_exc()}'
        logger.error(log_msg)
        return omni_services

    return omni_services
