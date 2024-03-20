from django import template

from base_app.settings import COUNTRY_CODES
from menumanager_country_api.settings.base import COUNTRY_CODE

register = template.Library()


@register.simple_tag
def get_current_country():
    country = COUNTRY_CODES.get(COUNTRY_CODE, False)
    return country if country else 'Unknown'
