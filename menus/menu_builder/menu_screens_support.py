from menus.models import MenuOption, NavigationLabel, UssdLabel
from menus.settings import BACK_NAVIGATION_TEXT_FALLBACK, DEFAULT_LANGUAGE_CODE, HOME_MENU_SCREEN, \
    MAIN_MENU_NAVIGATION_TEXT_FALLBACK, NAVIGATION_BACK_INPUT, NAVIGATION_BACK_TYPE, \
    NAVIGATION_HOME_INPUT, NAVIGATION_HOME_TYPE, PIN_RESET_NAVIGATION_TEXT_FALLBACK, PIN_RESET_SCREEN


def get_labels_qs(menu_obj):
    labels = UssdLabel.objects.filter(menu=menu_obj)
    if not labels.exists():
        raise AttributeError(
            f'Can not generate messages for "{menu_obj}". '
            f'No labels found (labels were: "{labels}"). '
            f'Have you forgot to activate menu labels ?')
    return labels


def get_labels_text(labels_qs, language):
    label_obj = labels_qs.filter(language=language)
    if not label_obj.exists():
        label_obj = labels_qs.filter(language__language_code=DEFAULT_LANGUAGE_CODE).first()
    else:
        label_obj = label_obj.first()
    return label_obj


def get_conditional_menu_options(menu_obj, languages):
    navigation_options = []

    if menu_obj.menu_screen_has_back:
        # generate all text languages
        back_navigation_text = {}
        for language in languages:
            try:
                menu_lang_obj = NavigationLabel.objects.get(language=language)
            except NavigationLabel.DoesNotExist:
                menu_lang_obj = None
            back_navigation_text[language.language_code] = BACK_NAVIGATION_TEXT_FALLBACK \
                if menu_lang_obj is None else menu_lang_obj.back_label
        if menu_obj.menu_screen_back_screen is not None:
            navigation_options.append({
                'text': back_navigation_text,
                'next_screen': menu_obj.menu_screen_back_screen.name,
                'input': NAVIGATION_BACK_INPUT,
                'type': NAVIGATION_BACK_TYPE,
            })
        else:
            navigation_options.append({
                'text': back_navigation_text,
                'next_screen': HOME_MENU_SCREEN,
                'input': False,
                '_note': 'Back navigation will be handled by the user session.',
                'type': NAVIGATION_BACK_TYPE,
            })

    if menu_obj.menu_screen_has_home:
        # generate all text languages
        home_navigation_text = {}
        for language in languages:
            try:
                menu_lang_obj = NavigationLabel.objects.get(language=language)
            except NavigationLabel.DoesNotExist:
                menu_lang_obj = None
            home_navigation_text[language.language_code] = MAIN_MENU_NAVIGATION_TEXT_FALLBACK \
                if menu_lang_obj is None else menu_lang_obj.main_menu_label

        navigation_options.append({
            'text': home_navigation_text,
            'next_screen': HOME_MENU_SCREEN,
            'input': NAVIGATION_HOME_INPUT,
            'type': NAVIGATION_HOME_TYPE,
        })
    return navigation_options


def get_menu_options(menu_obj, languages):
    menu_options = MenuOption.objects.filter(menu=menu_obj)
    if not menu_options.exists():
        raise AttributeError(f'No menu options defined for the menu: {menu_obj}')
    menu_screen_options = []

    # sort menus by ordering and language
    menus_by_ordering = {}
    for menu_option in menu_options:
        if menu_option.order not in menus_by_ordering:
            menus_by_ordering[menu_option.order] = {}
        for language in languages:
            lang_menu_option = menu_options.filter(language=language, order=menu_option.order).first()
            if lang_menu_option is None:
                lang_menu_option = menu_options.filter(
                    language__language_code=DEFAULT_LANGUAGE_CODE, order=menu_option.order).first()
            menus_by_ordering[menu_option.order][language.language_code] = lang_menu_option

    # get menu option text
    for order_number, ordered_menus in menus_by_ordering.items():
        menu_item = {'text': {}, 'next_screen': str(ordered_menus[list(ordered_menus)[0]].next_screen.name)}
        for language, ordered_menu in ordered_menus.items():
            menu_item['text'][language] = ordered_menu.option_text
        menu_screen_options.append(menu_item)
    return menu_screen_options


def get_conditional_next_screens(menu_obj):
    option_dict = {
        'condition': None,
        'next_screen': None,
    }
    options = []
    if menu_obj.input_screen_has_home:
        condition = option_dict.copy()
        condition['condition'] = 'input == "00"'
        condition['next_screen'] = HOME_MENU_SCREEN
        options.append(condition)
    if menu_obj.input_screen_has_back:
        condition = option_dict.copy()
        condition['condition'] = 'input == "0"'
        if menu_obj.input_screen_back_screen is not None:
            condition['next_screen'] = menu_obj.input_screen_back_screen.name
        else:
            condition['next_screen'] = HOME_MENU_SCREEN
            condition['_note'] = 'Back navigation will be handled by the user session.'
        options.append(condition)
    if menu_obj.input_screen_has_pin_reset:
        condition = option_dict.copy()
        condition['condition'] = 'input == "1"'
        condition['next_screen'] = PIN_RESET_SCREEN
        options.append(condition)
    return options


def get_input_screen_text(menu_obj, labels_qs, languages):
    result = {}
    for language in languages:
        label_obj = get_labels_text(labels_qs=labels_qs, language=language)
        label_str = label_obj.label_text.strip() + ' '
        try:
            menu_lang_obj = NavigationLabel.objects.get(language=language)
            lang_available_check = True
        except NavigationLabel.DoesNotExist:
            menu_lang_obj = None
            lang_available_check = False

        if menu_obj.input_screen_has_back:
            default_str = BACK_NAVIGATION_TEXT_FALLBACK
            if lang_available_check:
                label = menu_lang_obj.back_label if len(menu_lang_obj.back_label.strip()) != 0 else default_str
            else:
                label = default_str
            label_str += f'\n0. {label} '
        if menu_obj.input_screen_has_pin_reset:
            default_str = PIN_RESET_NAVIGATION_TEXT_FALLBACK
            if lang_available_check:
                label = menu_lang_obj.pin_reset_label if len(
                    menu_lang_obj.pin_reset_label.strip()) != 0 else default_str
            else:
                label = default_str
            label_str += f'\n1. {label} '
        if menu_obj.input_screen_has_home:
            default_str = MAIN_MENU_NAVIGATION_TEXT_FALLBACK
            if lang_available_check:
                label = menu_lang_obj.main_menu_label if len(
                    menu_lang_obj.main_menu_label.strip()) != 0 else default_str
            else:
                label = default_str
            label_str += f'\n00. {label} '
        result[language.language_code] = label_str

    return result
