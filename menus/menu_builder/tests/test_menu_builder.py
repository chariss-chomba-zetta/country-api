import logging
import random

from django.conf import settings
from rest_framework.test import APITestCase

from menus.menu_builder import build_menus, tools
from menus.menu_builder.exceptions import MenuGenerationException
from menus.menu_builder.menu_screens_support import get_labels_text
from menus.menu_builder.settings import FORBIDDEN_SESSION_KEYS
from menus.menu_builder.tests import model_factories as factories
from menus.menu_builder.tests.model_factories import MenuOptionFactory, OmniServiceFactory, RouterOptionFactory, \
    UssdMenuFactory
from menus.menu_builder.tools import get_menu_key
from menus.models import ErrorLabel, Language, MenuItem, MenuOption, NavigationLabel, UssdLabel, UssdMenu
from menus.settings import ALL_SCREEN_TYPES, BACK_NAVIGATION_TEXT_FALLBACK, DEFAULT_ERROR_MESSAGE, \
    DEFAULT_LANGUAGE_CODE, ERROR_MESSAGE_TEXT_FALLBACK, \
    FUNCTION_SCREEN_NAME, HOME_MENU_SCREEN, INITIAL_SCREEN_NAME, INPUT_SCREEN_NAME, \
    MAIN_MENU_NAVIGATION_TEXT_FALLBACK, MENU_SCREEN_NAME, NAVIGATION_BACK_INPUT, NAVIGATION_BACK_TYPE, \
    NAVIGATION_HOME_INPUT, NAVIGATION_HOME_TYPE, NAVIGATION_KEY, PIN_RESET_SCREEN, QUIT_SCREEN_NAME, ROUTER_SCREEN_NAME

logger = logging.getLogger('CountryApiLogger')


class TestMenuBuild(APITestCase):
    shortcodes = None
    languages = None
    inactive_language = None
    nav_labels = None
    error_labels = None
    menu_types = None
    quit_screen = None

    def setUp(self):
        self.create_shortcodes()
        self.create_languages_labels_errors()
        self.create_menu_types()
        self.quit_screen = self.create_quit_screen()
        self.main_menu = self.create_menu_screen(shortcode=self.shortcodes[0], name=HOME_MENU_SCREEN)
        self.create_menu_screen_options(menu_screen=self.main_menu)

    # --- SUPPORT ---
    @staticmethod
    def get_generated_menu_data_for_menu_screen(menu_obj):
        menus = build_menus()
        menu_key = get_menu_key(shortcode=menu_obj.shortcode.shortcode)
        return menus.get(menu_key, {}).get(menu_obj.name)

    @staticmethod
    def create_router_options(router_screen, next_screens_collection, are_active=False):
        result = [RouterOptionFactory(menu=router_screen, next_screen=item, is_active=are_active) for item in
                  next_screens_collection]
        return result

    def create_shortcodes(self):
        self.shortcodes = []
        for item in range(2):
            shortcode = factories.ShortCodeFactory()
            self.shortcodes.append(shortcode)
        logger.info('Added shortcodes: %s', str(self.shortcodes))

    def create_languages_labels_errors(self):
        # add default language, 2 other random languages and 1 language that is not active
        default_lang = factories.LanguageFactory(language_code=DEFAULT_LANGUAGE_CODE)
        self.languages = [default_lang]
        for item in range(2):
            lang = factories.LanguageFactory()
            self.languages.append(lang)
        self.inactive_lang = factories.LanguageFactory(is_active=False)

        self.nav_labels = []
        self.error_labels = []
        for lang in Language.objects.get_full_queryset().all():
            nav_label = factories.NavigationLabelFactory(language=lang)
            err_label = factories.ErrorLabelFactory(language=lang)
            self.nav_labels.append(nav_label)
            self.error_labels.append(err_label)

        logger.info('Added languages: %s', str(self.languages))
        logger.info('Added nav labels for languages: %s', str(self.nav_labels))
        logger.info('Added error labels for languages: %s', self.error_labels)

    def create_menu_types(self):
        self.menu_types = {}
        for item in ALL_SCREEN_TYPES:
            menu_type_obj = factories.MenuTypeFactory()
            self.menu_types[item] = menu_type_obj

    def create_labels_for_menu(self, menu_obj):
        for lang in self.languages:
            factories.UssdLabelFactory(menu=menu_obj, language=lang)

    def create_quit_screen(self, shortcode=None):
        quit_screen = UssdMenuFactory(
            menu_type=self.menu_types[QUIT_SCREEN_NAME],
            next_screen=None,
            omni_service=None,
            shortcode=shortcode if shortcode is not None else self.shortcodes[0],
        )
        self.create_labels_for_menu(quit_screen)
        return quit_screen

    def create_initial_screen(self, shortcode, next_screen=None):
        initial_screen = UssdMenuFactory(
            menu_type=self.menu_types[INITIAL_SCREEN_NAME],
            shortcode=shortcode,
            next_screen=next_screen if next_screen is not None else self.quit_screen,
            omni_service=None,
        )
        return initial_screen

    def create_input_screen(self, shortcode=None):
        input_screen = UssdMenuFactory(
            menu_type=self.menu_types[INPUT_SCREEN_NAME],
            next_screen=self.quit_screen,
            omni_service=None,
            shortcode=shortcode if shortcode is not None else self.shortcodes[0],
        )
        self.create_labels_for_menu(input_screen)
        return input_screen

    def create_function_screen(self, shortcode):
        omni_service = OmniServiceFactory()
        function_screen = UssdMenuFactory(
            menu_type=self.menu_types[FUNCTION_SCREEN_NAME],
            shortcode=shortcode,
            next_screen=self.quit_screen,
            omni_service=omni_service,
        )
        return function_screen, omni_service

    def create_menu_screen(self, shortcode=None, name=None, has_options=True):
        menu_screen = UssdMenuFactory(
            menu_type=self.menu_types[MENU_SCREEN_NAME],
            next_screen=None,
            omni_service=None,
            shortcode=shortcode if shortcode is not None else self.shortcodes[0],
            has_options=has_options,
        )
        if name is not None:
            menu_screen.name = name
        self.create_labels_for_menu(menu_screen)

        if not has_options:
            function_scr, omni_service = self.create_function_screen(shortcode=menu_screen.shortcode)
            factories.MenuItemFactory(ussd_menu=menu_screen)
            menu_screen.next_screen = function_scr
            menu_screen.save()
        return menu_screen

    def create_menu_screen_options(self, menu_screen):
        if not menu_screen.has_options:
            return
        counter = 1
        for item in range(3, 10):
            for lang in self.languages:
                MenuOptionFactory(
                    menu=menu_screen,
                    language=lang,
                    order=counter,
                    next_screen=self.create_quit_screen(shortcode=menu_screen.shortcode),
                )
            counter += 1
        return menu_screen

    def create_router_screen(self, shortcode=None):
        router_screen = UssdMenuFactory(
            menu_type=self.menu_types[ROUTER_SCREEN_NAME],
            shortcode=shortcode if shortcode is not None else self.shortcodes[0],
            next_screen=self.quit_screen,
            omni_service=None,
        )
        return router_screen

    def text_label_fallback_tester(self, menu_obj):
        # if no label for the given menu, generated text should be fallen back to the default
        label_qs = UssdLabel.objects.filter(menu=menu_obj)
        deleted_lang_code = label_qs.last().language.language_code
        label_qs.last().delete()
        screen_specs = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_obj)
        for lang in self.languages:
            message = screen_specs['text'][lang.language_code]
            message = message.split('\n')[0].strip()
            if lang.language_code == deleted_lang_code:
                default_message = label_qs.filter(language__language_code=DEFAULT_LANGUAGE_CODE).first().label_text
                self.assertEqual(message, default_message)
            else:
                label_message = label_qs.filter(language=lang).first().label_text
                self.assertEqual(message, label_message)

    def obj_label_fallback_tester(self, menu_obj):
        # does the same as text_label_fallback_tester but on obj level.
        # if no label obj for the given menu is available, screen label obj should be fallen back to the default
        label_qs = UssdLabel.objects.filter(menu=menu_obj)
        deleted_lang_code = label_qs.last().language.language_code
        label_qs.last().delete()
        for lang in self.languages:
            label_obj = get_labels_text(label_qs, lang)
            if lang.language_code == deleted_lang_code:
                self.assertEqual(
                    label_qs.filter(language__language_code=DEFAULT_LANGUAGE_CODE).first().pk,
                    label_obj.pk,
                )
            else:
                self.assertEqual(label_qs.filter(language=lang).first().pk, label_obj.pk)

    def missing_labels_tester(self, menu_obj):
        build_menus()
        label_qs = UssdLabel.objects.filter(menu=menu_obj)
        label_qs.delete()
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def menu_options_tester(self, menu_obj):
        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_obj)
        self.assertIsNotNone(menu_screen_data)
        self.assertEqual(menu_screen_data['type'], MENU_SCREEN_NAME)
        self.assertIn('options', list(menu_screen_data.keys()))

        order_item = 1
        menu_options_data = menu_screen_data['options']
        for menu_option in menu_options_data:
            self.assertIn('text', list(menu_option.keys()))
            self.assertIn('next_screen', list(menu_option.keys()))
            languages_keys = list(menu_option['text'].keys())
            pass_time = 0
            for language in self.languages:
                self.assertIn(language.language_code, languages_keys)
                option_obj = MenuOption.objects.filter(menu=menu_obj, language=language, order=order_item).first()
                # handle language fallback
                if option_obj is None:
                    option_obj = MenuOption.objects.filter(
                        menu=menu_obj,
                        language__language_code=DEFAULT_LANGUAGE_CODE,
                        order=order_item,
                    ).first()

                self.assertIsNotNone(option_obj)
                self.assertEqual(option_obj.option_text, menu_option['text'][language.language_code])
                if pass_time == 0:
                    self.assertEqual(option_obj.next_screen.name, menu_option['next_screen'])
                pass_time += 1

            order_item += 1

    def menu_screen_error_messages_tester(self, menu_obj):
        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_obj)
        self.assertIsNotNone(menu_screen_data)
        self.assertEqual(menu_screen_data['type'], MENU_SCREEN_NAME)
        self.assertIn('error_message', list(menu_screen_data.keys()))
        error_messages = menu_screen_data['error_message']

        for language in self.languages:
            self.assertIn(language.language_code, list(error_messages.keys()))
            error_message = ErrorLabel.objects.filter(language=language).first()
            if error_message is None:
                self.assertEqual(ERROR_MESSAGE_TEXT_FALLBACK, error_messages[language.language_code])
            else:
                self.assertEqual(error_message.error_message, error_messages[language.language_code])

    def menu_screen_check_and_get_navigation(self, menu_screen_data, navigation_type):
        self.assertIn(NAVIGATION_KEY, list(menu_screen_data.keys()))
        navigation_list = menu_screen_data[NAVIGATION_KEY]
        self.assertIsInstance(navigation_list, list)
        navigation = [item for item in navigation_list if item['type'] == navigation_type]
        self.assertEqual(len(navigation), 1)
        return navigation[0]

    def menu_screen_check_navigation_text(self, navigation_data):
        for language in self.languages:
            label = NavigationLabel.objects.filter(language=language).first()
            if navigation_data['type'] == NAVIGATION_HOME_TYPE:
                label_text = label.main_menu_label if label is not None else MAIN_MENU_NAVIGATION_TEXT_FALLBACK
            elif navigation_data['type'] == NAVIGATION_BACK_TYPE:
                label_text = label.back_label if label is not None else BACK_NAVIGATION_TEXT_FALLBACK
            else:
                raise AssertionError(
                    f'Provided navigation data has unknown type! '
                    f'Should be one of: [{", ".join([NAVIGATION_BACK_TYPE, NAVIGATION_HOME_TYPE])}] '
                    f'It was: {navigation_data["type"]}')

            self.assertEqual(label_text, navigation_data['text'][language.language_code])

    def menu_screen_back_screen_navigation_tester(self, menu_obj):
        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_obj)
        # conditional screens specs
        self.assertIn('conditional_screen_specs', list(menu_screen_data.keys()))
        self.assertTrue(menu_screen_data['conditional_screen_specs']['menu_screen_has_back'])
        if menu_obj.menu_screen_back_screen is not None:
            self.assertEqual(
                menu_screen_data['conditional_screen_specs']['menu_screen_back_screen'],
                menu_obj.menu_screen_back_screen.name,
            )
        else:
            self.assertIsNone(menu_screen_data['conditional_screen_specs']['menu_screen_back_screen'])
        # navigation options
        back_navigation = self.menu_screen_check_and_get_navigation(
            menu_screen_data=menu_screen_data,
            navigation_type=NAVIGATION_BACK_TYPE,
        )
        if menu_obj.menu_screen_back_screen is not None:
            self.assertEqual(back_navigation['next_screen'], menu_obj.menu_screen_back_screen.name)
            self.assertEqual(back_navigation['input'], NAVIGATION_BACK_INPUT)
            self.assertNotIn('_note', list(back_navigation.keys()))
        else:
            self.assertEqual(back_navigation['next_screen'], HOME_MENU_SCREEN)
            self.assertFalse(back_navigation['input'])
            self.assertIn('_note', list(back_navigation.keys()))
            self.assertEqual(back_navigation['_note'], 'Back navigation will be handled by the user session.')

    def menu_screen_home_screen_navigation_tester(self, menu_obj):
        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_obj)
        home_navigation = self.menu_screen_check_and_get_navigation(
            menu_screen_data=menu_screen_data,
            navigation_type=NAVIGATION_HOME_TYPE,
        )
        self.assertEqual(home_navigation['next_screen'], HOME_MENU_SCREEN)
        self.assertEqual(home_navigation['input'], NAVIGATION_HOME_INPUT)
        self.assertNotIn('_note', list(home_navigation.keys()))

    # --- ACTUAL TESTS ---

    def test_initialize_get_menu_key(self):
        shortcode = 123456
        result = tools.get_menu_key(shortcode=shortcode)
        expected = f'{settings.CACHE_MENU_KEY_PREFIX}_{settings.COUNTRY_CODE}_{shortcode}'
        self.assertEqual(result, expected)

    # --- INITIAL SCREEN ---
    def test_initial_screen(self):
        self.create_initial_screen(shortcode=self.shortcodes[0])
        all_menus = build_menus()
        menus = all_menus.get(tools.get_menu_key(shortcode=self.shortcodes[0]))
        self.assertEqual(menus['initial_screen']['next_screen'], self.quit_screen.name)
        self.assertEqual(len(all_menus.keys()), 1)

        # add another shortcode
        self.create_initial_screen(shortcode=self.shortcodes[1])
        all_menus = build_menus()
        self.assertEqual(len(all_menus.keys()), 2)
        self.assertIn(tools.get_menu_key(shortcode=self.shortcodes[1]), list(all_menus.keys()))

    def test_multiple_initial_screens(self):
        # add 2 input screens
        self.create_initial_screen(shortcode=self.shortcodes[0])
        build_menus()
        self.create_initial_screen(shortcode=self.shortcodes[0])
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def test_custom_quit_screen_is_added_on_initialization(self):
        for shortcode in self.shortcodes:
            self.create_initial_screen(shortcode=shortcode)
            menu_key = tools.get_menu_key(shortcode=shortcode)
            all_menus = build_menus().get(menu_key)
            custom_quit_screen_name = UssdMenu.generate_custom_error_screen_name(shortcode_obj=shortcode)
            self.assertIn(custom_quit_screen_name, list(all_menus.keys()))
            custom_quit_screen = all_menus[custom_quit_screen_name]
            self.assertEqual(custom_quit_screen['type'], QUIT_SCREEN_NAME)
            for label_lang in custom_quit_screen['text']:
                self.assertEqual(custom_quit_screen['text'][label_lang], DEFAULT_ERROR_MESSAGE)

    # --- QUIT SCREEN ---
    def test_quit_screen(self):
        other_quit_screen = self.create_quit_screen(shortcode=self.shortcodes[1])
        menus = build_menus()
        self.assertIn(self.quit_screen.name, menus.get(tools.get_menu_key(shortcode=self.shortcodes[0])))
        self.assertIn(other_quit_screen.name, menus.get(tools.get_menu_key(shortcode=self.shortcodes[1])))

        quit_screen = menus.get(tools.get_menu_key(shortcode=self.shortcodes[0])).get(self.quit_screen.name)
        self.assertEqual(quit_screen['type'], QUIT_SCREEN_NAME)
        label_qs = UssdLabel.objects.filter(menu=self.quit_screen)
        self.assertEqual(len(list(quit_screen['text'].keys())), 3)
        self.assertNotIn(self.inactive_lang.language_code, list(quit_screen['text'].keys()))
        for lang in self.languages:
            self.assertEqual(quit_screen['text'][lang.language_code], label_qs.filter(language=lang).first().label_text)

    def test_quit_screen_label_objects(self):
        self.obj_label_fallback_tester(menu_obj=self.quit_screen)

    def test_quit_screen_label_texts(self):
        self.text_label_fallback_tester(menu_obj=self.quit_screen)

    def test_quit_screen_no_labels(self):
        self.missing_labels_tester(menu_obj=self.quit_screen)

    # --- ROUTER SCREEN ---
    def test_router_screen(self):
        router_screen = self.create_router_screen()
        quit_screens = [self.create_quit_screen(shortcode=self.shortcodes[0]) for item in range(3)]
        self.create_initial_screen(shortcode=self.shortcodes[1])
        router_options = self.create_router_options(
            router_screen=router_screen,
            next_screens_collection=quit_screens,
            are_active=True,
        )
        inactive_option = router_options.pop()
        inactive_option.is_active = False
        inactive_option.save()
        router_options.append(inactive_option)
        menus = build_menus()
        # no active router options checks
        shortcode_1 = menus[tools.get_menu_key(shortcode=self.shortcodes[0])]
        shortcode_2 = menus[tools.get_menu_key(shortcode=self.shortcodes[1])]
        self.assertIn(router_screen.name, shortcode_1)
        self.assertNotIn(router_screen.name, shortcode_2)
        # specs checks
        specs = shortcode_1[router_screen.name]
        self.assertEqual(specs['type'], ROUTER_SCREEN_NAME)
        self.assertEqual(specs['default_next_screen'], self.quit_screen.name)

        # right option checks
        options = specs['router_options']
        self.assertEqual(len(options), 3)
        self.assertEqual(options[0]['expression'], router_options[0].menu_expression)
        self.assertEqual(options[0]['next_screen'], router_options[0].next_screen.name)
        self.assertEqual(options[1]['expression'], router_options[1].menu_expression)
        self.assertEqual(options[1]['next_screen'], router_options[1].next_screen.name)
        # check for default error option
        custom_quit_screen_name = router_screen.generate_custom_error_screen_name(shortcode_obj=self.shortcodes[0])
        self.assertEqual(options[2]['expression'], router_options[0].generate_custom_quit_screen_expression())
        self.assertEqual(options[2]['next_screen'], custom_quit_screen_name)

    def test_router_screen_no_or_inactive_router_options(self):
        router_screen = self.create_router_screen()
        quit_screens = [self.create_quit_screen(shortcode=self.shortcodes[0]) for item in range(3)]
        self.create_initial_screen(shortcode=self.shortcodes[1])
        with self.assertRaises(MenuGenerationException):
            build_menus()
        self.create_router_options(router_screen=router_screen, next_screens_collection=quit_screens)
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def test_no_next_screen_router_screen(self):
        router_screen = self.create_router_screen()
        self.create_initial_screen(shortcode=self.shortcodes[0])
        router_options = self.create_router_options(
            router_screen=router_screen,
            next_screens_collection=[self.quit_screen],
            are_active=True,
        )
        router_screen.next_screen = None
        router_screen.save()
        default_next_screen = self.get_generated_menu_data_for_menu_screen(menu_obj=router_screen).get(
            'default_next_screen')
        self.assertEqual(default_next_screen, router_options[0].generate_custom_quit_screen_expression())

    # --- FUNCTION SCREEN ---
    def test_function_screen_wrong(self):
        function_screen = UssdMenuFactory(
            menu_type=self.menu_types[FUNCTION_SCREEN_NAME],
            shortcode=self.shortcodes[0],
            next_screen=self.quit_screen,
            omni_service=None,
        )
        with self.assertRaises(MenuGenerationException):
            build_menus()
        omni_service = OmniServiceFactory()
        # forbidden session key
        key = FORBIDDEN_SESSION_KEYS[0]
        omni_service.session_key = key
        omni_service.save()
        function_screen.omni_service = omni_service
        function_screen.save()
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def test_function_screen_okay(self):
        # right shortcode
        function_screens = []
        omni_services = []
        for item in range(random.randint(10, 30)):
            temp_function_screen, temp_omni_service = self.create_function_screen(shortcode=self.shortcodes[0])
            function_screens.append(temp_function_screen)
            omni_services.append(temp_omni_service)
        # other shortcode
        other_function_screens = []
        other_omni_services = []
        for item in range(random.randint(10, 30)):
            temp_function_screen, temp_omni_service = self.create_function_screen(shortcode=self.shortcodes[1])
            other_function_screens.append(temp_function_screen)
            other_omni_services.append(temp_omni_service)

        all_menus = build_menus()

        # right shortcode
        menus = all_menus.get(tools.get_menu_key(shortcode=self.shortcodes[0]))
        for function_screen in function_screens:
            screen_specs = menus.get(function_screen.name)
            omni_service = omni_services[function_screens.index(function_screen)]
            self.assertEqual(screen_specs['type'], FUNCTION_SCREEN_NAME)
            self.assertEqual(screen_specs['function'], omni_service.service_function)
            self.assertEqual(screen_specs['session_key'], omni_service.session_key)
            self.assertEqual(screen_specs['next_screen'], function_screen.next_screen.name)
            self.assertEqual(screen_specs['default_next_screen'], function_screen.next_screen.name)
            if bool(omni_service.service_degradation_key):
                self.assertEqual(screen_specs['service_degradation_key'], omni_service.service_degradation_key)
            else:
                self.assertIsNone(screen_specs['service_degradation_key'])

        # other shortcode
        other_menus = all_menus.get(tools.get_menu_key(shortcode=self.shortcodes[1]))
        for function_screen in other_function_screens:
            screen_specs = menus.get(function_screen.name)
            self.assertIsNone(screen_specs)
            self.assertIn(function_screen.name, other_menus)

    # --- INPUT SCREEN ---
    def test_input_screen_label_texts(self):
        input_screen = self.create_input_screen(shortcode=self.shortcodes[0])
        self.text_label_fallback_tester(menu_obj=input_screen)

    def test_input_screen_label_objects(self):
        input_screen = self.create_input_screen(shortcode=self.shortcodes[0])
        self.obj_label_fallback_tester(menu_obj=input_screen)

    def test_input_screen_no_labels(self):
        input_screen = self.create_input_screen(shortcode=self.shortcodes[0])
        self.missing_labels_tester(menu_obj=input_screen)

    def test_input_screen_identifier_in_forbidden(self):
        input_screen = self.create_input_screen(shortcode=self.shortcodes[0])
        build_menus()
        input_screen.input_identifier = FORBIDDEN_SESSION_KEYS[0]
        input_screen.save()
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def test_input_screen_not_conditional(self):
        input_screens = []
        for item in range(random.randint(20, 40)):
            input_screen = self.create_input_screen(shortcode=self.shortcodes[0])
            input_screen.input_screen_has_back = False
            input_screen.input_screen_has_home = False
            input_screen.input_screen_has_pin_reset = False
            if random.choice([True, False]):
                input_screen.input_screen_back_screen = self.quit_screen
            input_screen.save()
            input_screens.append(input_screen)
        all_menus = build_menus()
        menus = all_menus.get(tools.get_menu_key(shortcode=self.shortcodes[0]))

        for input_screen in input_screens:
            conditional_screen_specs = menus[input_screen.name]['conditional_screen_specs']
            self.assertFalse(conditional_screen_specs['input_screen_has_back'])
            self.assertIsNone(conditional_screen_specs['input_screen_back_screen'])
            self.assertIsInstance(menus[input_screen.name]['next_screen'], str)

    def test_input_screen_has_back(self):
        input_screens = []
        other_quit_screen = self.create_quit_screen()
        counter = 0
        for item in range(random.randint(20, 40)):
            input_screen = self.create_input_screen(shortcode=self.shortcodes[0])
            input_screen.next_screen = other_quit_screen
            input_screen.input_screen_has_back = True
            input_screen.input_screen_has_home = False
            input_screen.input_screen_has_pin_reset = False
            if counter % 2 == 0:
                input_screen.input_screen_back_screen = self.quit_screen
            input_screen.save()
            input_screens.append(input_screen)
            counter += 1

        for input_screen in input_screens:
            menu_data = self.get_generated_menu_data_for_menu_screen(menu_obj=input_screen)
            next_screen_specs = menu_data['next_screen']
            self.assertIsInstance(next_screen_specs, list)
            self.assertIsInstance(next_screen_specs[0], dict)
            self.assertEqual(len(next_screen_specs), 1)
            self.assertEqual(menu_data['default_next_screen'], other_quit_screen.name)
            conditional_screen_specs = menu_data['conditional_screen_specs']
            self.assertTrue(conditional_screen_specs['input_screen_has_back'])

            detail_specs = next_screen_specs[0]
            self.assertEqual(detail_specs['condition'], 'input == "0"')
            if input_screen.input_screen_back_screen is not None:
                self.assertEqual(detail_specs['next_screen'], input_screen.input_screen_back_screen.name)
                self.assertNotIn('_note', detail_specs)
            else:
                self.assertEqual(detail_specs['next_screen'], HOME_MENU_SCREEN)
                self.assertIn('_note', detail_specs)
                self.assertEqual(detail_specs['_note'], 'Back navigation will be handled by the user session.')

    def test_input_screen_has_home(self):
        input_screens = []
        other_quit_screen = self.create_quit_screen()
        for item in range(random.randint(20, 40)):
            input_screen = self.create_input_screen(shortcode=self.shortcodes[0])
            input_screen.next_screen = other_quit_screen
            input_screen.input_screen_has_back = False
            input_screen.input_screen_has_home = True
            input_screen.input_screen_has_pin_reset = False
            input_screen.save()
            input_screens.append(input_screen)

        for input_screen in input_screens:
            menu_data = self.get_generated_menu_data_for_menu_screen(menu_obj=input_screen)
            next_screen_specs = menu_data['next_screen']
            self.assertIsInstance(next_screen_specs, list)
            self.assertIsInstance(next_screen_specs[0], dict)
            self.assertEqual(len(next_screen_specs), 1)
            self.assertEqual(menu_data['default_next_screen'], other_quit_screen.name)
            conditional_screen_specs = menu_data['conditional_screen_specs']
            self.assertFalse(conditional_screen_specs['input_screen_has_back'])
            self.assertIsNone(conditional_screen_specs['input_screen_back_screen'])

            detail_specs = next_screen_specs[0]
            self.assertEqual(detail_specs['condition'], 'input == "00"')
            self.assertEqual(detail_specs['next_screen'], HOME_MENU_SCREEN)

    def test_input_screen_has_pin_reset(self):
        input_screens = []
        other_quit_screen = self.create_quit_screen()
        for item in range(random.randint(20, 40)):
            input_screen = self.create_input_screen(shortcode=self.shortcodes[0])
            input_screen.next_screen = other_quit_screen
            input_screen.input_screen_has_back = False
            input_screen.input_screen_has_home = False
            input_screen.input_screen_has_pin_reset = True
            input_screen.save()
            input_screens.append(input_screen)

        for input_screen in input_screens:
            menu_data = self.get_generated_menu_data_for_menu_screen(menu_obj=input_screen)
            next_screen_specs = menu_data['next_screen']
            self.assertIsInstance(next_screen_specs, list)
            self.assertIsInstance(next_screen_specs[0], dict)
            self.assertEqual(len(next_screen_specs), 1)
            self.assertEqual(menu_data['default_next_screen'], other_quit_screen.name)
            conditional_screen_specs = menu_data['conditional_screen_specs']
            self.assertFalse(conditional_screen_specs['input_screen_has_back'])
            self.assertIsNone(conditional_screen_specs['input_screen_back_screen'])

            detail_specs = next_screen_specs[0]
            self.assertEqual(detail_specs['condition'], 'input == "1"')
            self.assertEqual(detail_specs['next_screen'], PIN_RESET_SCREEN)

    # --- MENU SCREEN ---
    # common
    def test_menu_screen_error_messages(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        self.create_menu_screen_options(menu_screen=menu_screen)
        self.menu_screen_error_messages_tester(menu_obj=menu_screen)
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        self.menu_screen_error_messages_tester(menu_obj=menu_screen)

    def test_menu_screen_error_messages_fallback(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        self.create_menu_screen_options(menu_screen=menu_screen)
        ErrorLabel.objects.filter(language=random.choice(list(self.languages[1:]))).first().delete()
        self.menu_screen_error_messages_tester(menu_obj=menu_screen)

    def test_menu_screen_no_conditional_screens_specs(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_back = False
        menu_screen.menu_screen_has_home = False
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)
        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_screen)
        self.assertIn('conditional_screen_specs', list(menu_screen_data.keys()))
        self.assertFalse(menu_screen_data['conditional_screen_specs']['menu_screen_has_back'])
        self.assertIsNone(menu_screen_data['conditional_screen_specs']['menu_screen_back_screen'])
        self.assertNotIn(NAVIGATION_KEY, list(menu_screen_data.keys()))

    def test_menu_screen_no_navigation(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_home = False
        menu_screen.menu_screen_has_back = False
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)
        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_screen)
        self.assertNotIn(NAVIGATION_KEY, list(menu_screen_data.keys()))
        self.assertIn('conditional_screen_specs', list(menu_screen_data.keys()))

    # labelling
    def test_menu_screen_label_texts_with_options(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        self.create_menu_screen_options(menu_screen=menu_screen)
        self.text_label_fallback_tester(menu_obj=menu_screen)

    def test_menu_screen_label_objects_with_options(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        self.create_menu_screen_options(menu_screen=menu_screen)
        self.obj_label_fallback_tester(menu_obj=menu_screen)

    def test_menu_screen_no_labels_with_options(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        self.create_menu_screen_options(menu_screen=menu_screen)
        self.missing_labels_tester(menu_obj=menu_screen)

    def test_menu_screen_label_texts_without_options(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        self.text_label_fallback_tester(menu_obj=menu_screen)

    def test_menu_screen_label_objects_without_options(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        self.obj_label_fallback_tester(menu_obj=menu_screen)

    def test_menu_screen_no_labels_without_options(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        self.missing_labels_tester(menu_obj=menu_screen)

    # navigation labels tests
    def test_menu_screen_back_label_texts(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_back = True
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)
        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_screen)
        back_navigation = self.menu_screen_check_and_get_navigation(
            menu_screen_data=menu_screen_data,
            navigation_type=NAVIGATION_BACK_TYPE,
        )
        self.menu_screen_check_navigation_text(navigation_data=back_navigation)

    def test_menu_screen_back_label_texts_fallback(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_back = True
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)

        NavigationLabel.objects.exclude(language__language_code=DEFAULT_LANGUAGE_CODE).first().delete()

        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_screen)
        back_navigation = self.menu_screen_check_and_get_navigation(
            menu_screen_data=menu_screen_data,
            navigation_type=NAVIGATION_BACK_TYPE,
        )
        self.menu_screen_check_navigation_text(navigation_data=back_navigation)

    def test_menu_screen_home_label_texts(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_home = True
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)
        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_screen)
        home_navigation = self.menu_screen_check_and_get_navigation(
            menu_screen_data=menu_screen_data,
            navigation_type=NAVIGATION_HOME_TYPE,
        )
        self.menu_screen_check_navigation_text(navigation_data=home_navigation)

    def test_menu_screen_home_label_texts_fallback(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_home = True
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)

        NavigationLabel.objects.exclude(language__language_code=DEFAULT_LANGUAGE_CODE).first().delete()

        menu_screen_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_screen)
        home_navigation = self.menu_screen_check_and_get_navigation(
            menu_screen_data=menu_screen_data,
            navigation_type=NAVIGATION_HOME_TYPE,
        )
        self.menu_screen_check_navigation_text(navigation_data=home_navigation)

    # menus with options tests
    def test_menu_screen_with_options_missing_options(self):
        self.create_menu_screen(shortcode=self.shortcodes[0])
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def test_menu_screen_with_options_check_options_are_correct(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        self.create_menu_screen_options(menu_screen=menu_screen)
        self.menu_options_tester(menu_obj=menu_screen)

    def test_menu_screen_with_options_fallback_language_support(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        self.create_menu_screen_options(menu_screen=menu_screen)
        # will delete one element and keep one. Others will be deleted on a random
        MenuOption.objects.filter(
            menu=menu_screen,
        ).exclude(
            language__language_code=DEFAULT_LANGUAGE_CODE,
        ).first().delete()

        menu_options = MenuOption.objects.filter(
            menu=menu_screen,
        ).exclude(
            language__language_code=DEFAULT_LANGUAGE_CODE,
        )
        for menu_option in menu_options[1:]:
            if random.choice([True, False]):
                menu_option.delete()

        self.menu_options_tester(menu_obj=menu_screen)

    def test_menu_screen_with_options_back_navigation_without_back_screen(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_back = True
        menu_screen.menu_screen_back_screen = None
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)
        self.menu_screen_back_screen_navigation_tester(menu_obj=menu_screen)

    def test_menu_screen_with_options_back_navigation_with_back_screen(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_back = True
        if menu_screen.menu_screen_back_screen is None:
            menu_screen.menu_screen_back_screen = self.quit_screen
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)
        self.menu_screen_back_screen_navigation_tester(menu_obj=menu_screen)

    def test_menu_screen_with_options_main_menu_navigation(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0])
        menu_screen.menu_screen_has_home = True
        menu_screen.save()
        self.create_menu_screen_options(menu_screen=menu_screen)
        self.menu_screen_home_screen_navigation_tester(menu_obj=menu_screen)

    # menus without options tests
    def test_menu_screen_without_options_no_menu_items(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        menu_item = MenuItem.objects.get(ussd_menu=menu_screen)
        build_menus()
        menu_item.delete()
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def test_menu_screen_without_options_more_than_one_menu_items(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        for item in range(random.randint(2, 6)):
            factories.MenuItemFactory(ussd_menu=menu_screen)
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def test_menu_screen_without_options_identifier_in_forbidden(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        menu_item = MenuItem.objects.get(ussd_menu=menu_screen)
        build_menus()
        menu_item.session_key = FORBIDDEN_SESSION_KEYS[0]
        menu_item.save()
        with self.assertRaises(MenuGenerationException):
            build_menus()

    def test_menu_screen_without_options_menu_data_is_okay(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        menu_item_obj = menu_screen.menu_item_parent_screen.all().first()
        menu_data = self.get_generated_menu_data_for_menu_screen(menu_obj=menu_screen)
        self.assertEqual(menu_data['type'], MENU_SCREEN_NAME)
        items_data = menu_data['items']
        self.assertIsInstance(items_data, dict)
        self.assertEqual(items_data['text'], menu_item_obj.item_text)
        self.assertEqual(items_data['value'], menu_item_obj.item_value)
        self.assertEqual(items_data['with_items'], menu_item_obj.with_items)
        self.assertEqual(items_data['session_key'], menu_item_obj.session_key)
        self.assertEqual(items_data['next_screen'], menu_screen.next_screen.name)

    def test_menu_screen_without_options_back_navigation_without_back_screen(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        menu_screen.menu_screen_has_back = True
        menu_screen.menu_screen_back_screen = None
        menu_screen.save()
        self.menu_screen_back_screen_navigation_tester(menu_obj=menu_screen)

    def test_menu_screen_without_options_back_navigation_with_back_screen(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        menu_screen.menu_screen_has_back = True
        if menu_screen.menu_screen_back_screen is None:
            menu_screen.menu_screen_back_screen = self.quit_screen
        menu_screen.save()
        self.menu_screen_back_screen_navigation_tester(menu_obj=menu_screen)

    def test_menu_screen_without_options_main_menu_navigation(self):
        menu_screen = self.create_menu_screen(shortcode=self.shortcodes[0], has_options=False)
        menu_screen.menu_screen_has_home = True
        menu_screen.save()
        self.menu_screen_home_screen_navigation_tester(menu_obj=menu_screen)
