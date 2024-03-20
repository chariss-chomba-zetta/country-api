import logging
import random

import faker
from rest_framework.test import APITestCase

from menus.menu_builder.tests import model_factories as factories
from menus.menu_builder.tests.model_factories import RouterOptionFactory, UssdLabelFactory, UssdMenuFactory
from menus.models import Language, MenuType, RouterOption, UssdLabel, UssdMenu
from menus.settings import ALL_SCREEN_TYPES, DEFAULT_ERROR_MESSAGE, DEFAULT_LANGUAGE_CODE, QUIT_SCREEN_NAME, \
    ROUTER_SCREEN_NAME

logger = logging.getLogger('CountryApiLogger')
fake = faker.Faker()


class BaseMenusTestClass(APITestCase):
    shortcode = None

    @staticmethod
    def create_menu_types():
        for item in ALL_SCREEN_TYPES:
            factories.MenuTypeFactory()

    @staticmethod
    def create_language(language_code=None):
        if language_code is not None:
            lang = factories.LanguageFactory(language_code=language_code)
        else:
            lang = factories.LanguageFactory()
        return lang

    def create_shortcode(self):
        self.shortcode = factories.ShortCodeFactory()


class TestCustomQuitScreenCreation(BaseMenusTestClass):

    def setUp(self):
        self.create_shortcode()
        self.create_menu_types()

    def test_missing_quit_screen_type(self):
        MenuType.objects.get(name=QUIT_SCREEN_NAME).delete()
        with self.assertRaises(RuntimeError):
            UssdMenu.create_custom_quit_screen(shortcode_obj=self.shortcode)

    def test_menu_is_created(self):
        quit_screen_type = MenuType.objects.get(name=QUIT_SCREEN_NAME)
        self.create_language(language_code=DEFAULT_LANGUAGE_CODE)
        UssdMenu.create_custom_quit_screen(shortcode_obj=self.shortcode)
        name = UssdMenu.generate_custom_error_screen_name(shortcode_obj=self.shortcode)
        obj = UssdMenu.objects.get_full_queryset().filter(name=name).first()
        self.assertIsNotNone(obj)
        self.assertEqual(obj.shortcode, self.shortcode)
        self.assertEqual(obj.menu_type, quit_screen_type)
        self.assertIsNone(obj.next_screen)
        self.assertTrue(obj.is_active)

    def test_handle_multiple_shortcodes(self):
        self.create_menu_types()
        self.create_language(language_code=DEFAULT_LANGUAGE_CODE)
        for item in range(random.randint(10, 30)):
            shortcode = factories.ShortCodeFactory()
            shortcode.save()
            try:
                UssdMenu.create_custom_quit_screen(shortcode_obj=shortcode)
            except Exception as exp:
                raise AssertionError(f'Count not build a custom quit screens for shortcode: {shortcode}') from exp

    def test_only_one_menu_is_created(self):
        self.create_menu_types()
        self.create_language(language_code=DEFAULT_LANGUAGE_CODE)
        obj_1 = UssdMenu.create_custom_quit_screen(shortcode_obj=self.shortcode)
        obj_2 = UssdMenu.create_custom_quit_screen(shortcode_obj=self.shortcode)
        count = UssdMenu.objects.get_full_queryset().filter(
            name=obj_1.generate_custom_error_screen_name(shortcode_obj=self.shortcode)).count()
        self.assertEqual(count, 1)
        self.assertEqual(obj_1.pk, obj_2.pk)
        self.assertEqual(
            obj_1.generate_custom_error_screen_name(shortcode_obj=self.shortcode),
            obj_2.generate_custom_error_screen_name(shortcode_obj=self.shortcode),
        )

    def test_missing_default_language(self):
        self.create_menu_types()
        with self.assertRaises(Language.DoesNotExist):
            UssdMenu.create_custom_quit_screen(shortcode_obj=self.shortcode)

    def test_labels_are_created(self):
        self.create_menu_types()
        self.create_language(language_code=DEFAULT_LANGUAGE_CODE)
        # call it twice to assure only one label is going to be created
        UssdMenu.create_custom_quit_screen(shortcode_obj=self.shortcode)
        obj = UssdMenu.create_custom_quit_screen(shortcode_obj=self.shortcode)
        # tests
        qs = UssdLabel.objects.filter(menu=obj)
        self.assertEqual(qs.count(), 1)
        # only for default language label is created
        self.create_language()
        qs = UssdLabel.objects.filter(menu=obj)
        self.assertEqual(qs.count(), 1)
        # verify message
        self.assertEqual(qs.first().label_text, DEFAULT_ERROR_MESSAGE)


class RouterOptionMenuExpressionToolboxFunctions(BaseMenusTestClass):
    router_screen = None
    language = None
    router_option = None
    expression_session_key = None
    expression_value = None
    expression_operator = None

    def setUp(self) -> None:
        self.create_shortcode()
        self.create_menu_types()
        self.language = self.create_language(language_code=DEFAULT_LANGUAGE_CODE)
        self.router_screen = UssdMenuFactory(
            menu_type=MenuType.objects.get(name=ROUTER_SCREEN_NAME),
            next_screen=None,
            omni_service=None,
            shortcode=self.shortcode,
        )
        expression = self.generate_expression()
        UssdLabelFactory(menu=self.router_screen, language=self.language)
        self.router_option = RouterOptionFactory(menu=self.router_screen, is_active=True, menu_expression=expression)

    def generate_expression(self):
        words1 = [word.lower() for word in fake.words(2)]
        words2 = [word.lower() for word in fake.words(4)]
        self.expression_session_key = f'{"_".join(words1)}.{"_".join(words2)}'
        self.expression_value = random.choice(['00', '99', '50'])
        self.expression_operator = random.choice(RouterOption.COMPARISON_OPERATORS)
        expression = f'{{{{{self.expression_session_key}{self.expression_operator}\'{self.expression_value}\'}}}}'
        return expression

    def test_menu_expression_comparison_operator(self):
        self.assertEqual(self.expression_operator, self.router_option.menu_expression_comparison_operator)

    def test_menu_expression_session_key(self):
        self.assertEqual(self.expression_session_key, self.router_option.menu_expression_session_key)

    def test_menu_expression_value(self):
        self.assertEqual(self.expression_value, self.router_option.menu_expression_value)
