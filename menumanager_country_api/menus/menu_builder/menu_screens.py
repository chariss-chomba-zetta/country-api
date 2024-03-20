from menus.menu_builder.decorators import screen_check_decorator
from menus.menu_builder.menu_screens_support import get_conditional_menu_options, get_conditional_next_screens, \
    get_input_screen_text, get_labels_qs, get_labels_text, get_menu_options
from menus.menu_builder.tools import check_session_key_in_forbidden_list, initialize_dict_response
from menus.models import MenuItem, RouterOption
from menus.settings import NAVIGATION_KEY

__all__ = ['initial_screen', 'input_screen', 'quit_screen', 'function_screen', 'menu_screen', 'router_screen']


def _add_conditional_screen_specs(menu_obj, menu_screen_specs):
    conditional_screen_specs = {
        'input_screen_has_back': menu_obj.input_screen_has_back,
        'input_screen_back_screen': menu_obj.input_screen_back_screen.name \
            if menu_obj.input_screen_has_back and menu_obj.input_screen_back_screen else None,
        'menu_screen_has_back': menu_obj.menu_screen_has_back,
        'menu_screen_back_screen': menu_obj.menu_screen_back_screen.name \
            if menu_obj.menu_screen_has_back and menu_obj.menu_screen_back_screen else None,
    }
    menu_screen = menu_screen_specs.copy()
    menu_screen['conditional_screen_specs'] = conditional_screen_specs

    return menu_screen


@screen_check_decorator
def initial_screen(menu_obj) -> dict:
    next_screen = menu_obj.next_screen.name
    menu_screen_specs = initialize_dict_response(menu_obj)
    menu_screen_specs['next_screen'] = next_screen

    return menu_screen_specs


@screen_check_decorator
def quit_screen(menu_obj, languages, error_messages) -> dict:
    menu_screen_specs = initialize_dict_response(menu_obj)
    labels = get_labels_qs(menu_obj)
    menu_screen_specs['text'] = {
        language.language_code: get_labels_text(labels, language=language).label_text for
        language in languages}
    return menu_screen_specs


@screen_check_decorator
def function_screen(menu_obj) -> dict:
    menu_screen_specs = initialize_dict_response(menu_obj)
    if check_session_key_in_forbidden_list(menu_obj.omni_service.session_key):
        raise ValueError(
            f'Function screen session key is in the < FORBIDDEN_SESSION_KEYS > list. '
            f'Screen is: {menu_obj} -> pk: {menu_obj.pk} | '
            f'Check Omni services for: {menu_obj.omni_service} -> '
            f'key is: {menu_obj.omni_service.session_key}, '
            f'pk is: {menu_obj.omni_service.pk}'
        )
    menu_screen_specs['function'] = menu_obj.omni_service.service_function
    menu_screen_specs['session_key'] = menu_obj.omni_service.session_key
    menu_screen_specs['next_screen'] = menu_obj.next_screen.name
    menu_screen_specs['default_next_screen'] = menu_obj.next_screen.name
    menu_screen_specs['service_degradation_key'] = menu_obj.omni_service.service_degradation_key if bool(
        menu_obj.omni_service.service_degradation_key) else None
    return menu_screen_specs


@screen_check_decorator
def router_screen(menu_obj) -> dict:
    router_screen_options = []
    routers = RouterOption.objects.filter(menu=menu_obj)
    if not routers.exists():
        raise AttributeError(f'{menu_obj} does not have any routers')
    for router in routers:
        menu_item = {
            'expression': router.menu_expression,
            'next_screen': router.next_screen.name
        }
        router_screen_options.append(menu_item)
    # handle custom error quit screen option
    quit_screen_expression = routers.first().generate_custom_quit_screen_expression()
    menu_item = {
        'expression': quit_screen_expression,
        'next_screen': menu_obj.custom_error_screen_name
    }
    router_screen_options.append(menu_item)

    menu_screen_specs = initialize_dict_response(menu_obj)
    next_screen = menu_obj.next_screen
    # assure that there is always default_next_screen.
    # If missing, the custom error screen will be used.
    # This way the journey will complete and will not end with exception.
    menu_screen_specs['default_next_screen'] = next_screen.name if next_screen is not None else quit_screen_expression
    menu_screen_specs['router_options'] = router_screen_options

    return menu_screen_specs


@screen_check_decorator
def input_screen(menu_obj, languages, error_messages):
    if check_session_key_in_forbidden_list(menu_obj.input_identifier):
        raise ValueError(
            f'Input screen input_identifier is in the < FORBIDDEN_SESSION_KEYS > list. '
            f'Screen is: {menu_obj} -> pk: {menu_obj.pk}, '
            f'key is: {menu_obj.input_identifier}'
        )
    menu_screen_specs = initialize_dict_response(menu_obj)
    labels = get_labels_qs(menu_obj)

    menu_screen_specs['text'] = get_input_screen_text(menu_obj=menu_obj, labels_qs=labels, languages=languages)
    menu_screen_specs['input_identifier'] = menu_obj.input_identifier

    if menu_obj.has_conditional_input_screens():
        menu_screen_specs['next_screen'] = get_conditional_next_screens(menu_obj=menu_obj)
        menu_screen_specs['default_next_screen'] = menu_obj.next_screen.name
    else:
        menu_screen_specs['next_screen'] = menu_obj.next_screen.name

    menu_screen_specs = _add_conditional_screen_specs(menu_obj=menu_obj, menu_screen_specs=menu_screen_specs)
    return menu_screen_specs


@screen_check_decorator
def menu_screen(menu_obj, languages, error_messages):
    menu_screen_specs = initialize_dict_response(menu_obj)
    labels = get_labels_qs(menu_obj)

    menu_screen_specs['text'] = {lang.language_code: get_labels_text(labels, language=lang).label_text for lang in
                                 languages}
    menu_screen_specs['error_message'] = error_messages

    if menu_obj.has_options:
        menu_screen_specs['options'] = get_menu_options(menu_obj, languages=languages)
    else:
        menu_screen_items = list(MenuItem.objects.filter(ussd_menu=menu_obj))
        if len(menu_screen_items) != 1:
            raise AttributeError(
                f'Menu screen: {menu_obj} should have exactly 1 MenuItem obj. '
                f'It has {len(menu_screen_items)}!')
        menu_screen_item = menu_screen_items[0]
        if check_session_key_in_forbidden_list(menu_screen_item.session_key):
            raise ValueError(
                f'Menu screen session key is in the < FORBIDDEN_SESSION_KEYS > list. '
                f'Screen is: {menu_obj} -> pk: {menu_obj.pk} | '
                f'Check menu item: {str(menu_screen_item)}, pk: {menu_screen_item.pk}, '
                f'key is: {menu_screen_item.session_key}'
            )

        menu_item_object = {
            'text': menu_screen_item.item_text,
            'value': menu_screen_item.item_value,
            'with_items': menu_screen_item.with_items,
            'session_key': menu_screen_item.session_key,
            'next_screen': menu_obj.next_screen.name,
        }

        menu_screen_specs['items'] = menu_item_object

    # handle conditional menus
    if menu_obj.has_conditional_menu_screens():
        navigation_options = get_conditional_menu_options(menu_obj=menu_obj, languages=languages)
        menu_screen_specs[NAVIGATION_KEY] = navigation_options

    menu_screen_specs = _add_conditional_screen_specs(menu_obj=menu_obj, menu_screen_specs=menu_screen_specs)
    return menu_screen_specs
