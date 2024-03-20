import random

import factory
import faker
from factory.django import DjangoModelFactory

import menus.models as models
from menus.menu_builder.tests.languages import TEST_LANGUAGES
from menus.settings import ALL_SCREEN_TYPES, INPUT_SCREEN_NAME, MENU_SCREEN_NAME, ROUTER_SCREEN_NAME

fake = faker.Faker()


def camel_case_generator(words=4):
    generated_words = [word.capitalize() for word in fake.words(words)]
    generated_words[0] = generated_words[0].lower()
    return ''.join(generated_words)


class ShortCodeFactory(DjangoModelFactory):
    class Meta:
        model = models.ShortCode

    institution = factory.Faker('company')
    shortcode = factory.LazyFunction(lambda: str(fake.random_number(digits=3)))
    country = factory.Faker('country_code')
    is_active = True


class MenuTypeFactory(DjangoModelFactory):
    class Meta:
        model = models.MenuType

    name = factory.Iterator(ALL_SCREEN_TYPES)


class LanguageFactory(DjangoModelFactory):
    class Meta:
        model = models.Language

    language_name = factory.LazyAttribute(lambda obj: TEST_LANGUAGES.get(obj.language_code))
    is_active = True

    @factory.lazy_attribute
    def language_code(self):
        while True:
            language_code = random.choice(list(TEST_LANGUAGES))
            if not models.Language.objects.filter(language_code=language_code).exists():
                break
        return language_code


class NavigationLabelFactory(DjangoModelFactory):
    class Meta:
        model = models.NavigationLabel

    language = factory.LazyFunction(lambda: random.choice(models.Language.objects.get_full_queryset().all()))
    back_label = factory.LazyAttribute(lambda obj: f'back_for__{obj.language.language_code}')
    main_menu_label = factory.LazyAttribute(lambda obj: f'main_menu_for__{obj.language.language_code}')
    pin_reset_label = factory.LazyAttribute(lambda obj: f'pin_reset_for__{obj.language.language_code}')


class ErrorLabelFactory(DjangoModelFactory):
    class Meta:
        model = models.ErrorLabel

    language = factory.LazyFunction(lambda: random.choice(models.Language.objects.get_full_queryset().all()))
    error_message = factory.LazyAttribute(lambda obj: f'error_message_for__{obj.language.language_code}')


class OmniServiceFactory(DjangoModelFactory):
    class Meta:
        model = models.OmniService

    url = factory.Faker('uri')
    method = factory.LazyFunction(lambda: random.choice(models.OmniService.MethodChoices.choices))
    session_key = factory.LazyFunction(lambda: '_'.join(fake.words(2)).lower())

    @factory.lazy_attribute
    def name(self):
        return camel_case_generator(4)

    @factory.lazy_attribute
    def service_function(self):
        words1 = [word.lower() for word in fake.words(2)]
        words2 = [word.lower() for word in fake.words(4)]
        return f'{"_".join(words1)}.{"_".join(words2)}'

    @factory.lazy_attribute
    def service_degradation_key(self):
        if random.choice([True, False]):
            return '_'.join([word.lower() for word in fake.words(2)])
        return ''


class UssdMenuFactory(DjangoModelFactory):
    class Meta:
        model = models.UssdMenu

    @factory.lazy_attribute
    def name(self):
        name = f'{camel_case_generator(6)}Screen'
        return name.capitalize()

    menu_type = factory.LazyFunction(lambda: random.choice(models.MenuType.objects.all()))
    shortcode = factory.LazyFunction(lambda: random.choice(models.ShortCode.objects.all()))
    next_screen = factory.LazyFunction(lambda: random.choice(models.UssdMenu.objects.all()))
    omni_service = factory.LazyFunction(lambda: random.choice(models.OmniService.objects.all()))
    has_options = factory.LazyAttribute(
        lambda obj: random.choice([True, False]) if obj.menu_type.name == MENU_SCREEN_NAME else False)
    input_identifier = factory.LazyAttribute(
        lambda obj: f'{"_".join([word.lower() for word in fake.words(2)])}'
        if obj.menu_type.name == INPUT_SCREEN_NAME else '')

    input_screen_has_back = factory.LazyAttribute(
        lambda obj: random.choice([True, False]) if obj.menu_type.name == INPUT_SCREEN_NAME else False)
    input_screen_back_screen = factory.LazyAttribute(
        lambda obj: random.choice(models.UssdMenu.objects.all()) if obj.input_screen_has_back else None)
    input_screen_has_home = factory.LazyAttribute(
        lambda obj: random.choice([True, False]) if obj.menu_type.name == INPUT_SCREEN_NAME else False)
    input_screen_has_pin_reset = factory.LazyAttribute(
        lambda obj: random.choice([True, False]) if obj.menu_type.name == INPUT_SCREEN_NAME else False)

    menu_screen_has_back = factory.LazyAttribute(
        lambda obj: random.choice([True, False]) if obj.menu_type.name == MENU_SCREEN_NAME else False)
    menu_screen_back_screen = factory.LazyAttribute(
        lambda obj: random.choice(models.UssdMenu.objects.all()) if obj.menu_screen_has_back else None)
    menu_screen_has_home = factory.LazyAttribute(
        lambda obj: random.choice([True, False]) if obj.menu_type.name == MENU_SCREEN_NAME else False)
    is_active = True


class UssdLabelFactory(DjangoModelFactory):
    class Meta:
        model = models.UssdLabel

    menu = factory.LazyFunction(lambda: random.choice(models.UssdMenu.objects.all()))
    language = factory.LazyFunction(lambda: random.choice(models.Language.objects.all()))
    label_text = factory.LazyFunction(lambda: ' '.join([word.capitalize() for word in fake.words(6)]))


class MenuItemFactory(DjangoModelFactory):
    class Meta:
        model = models.MenuItem

    item_text = factory.LazyFunction(
        lambda: '{{{{ {} }}}}'.format('.'.join([word.lower() for word in fake.words(2)])))
    item_value = factory.LazyFunction(
        lambda: f'{{{{ {".".join([word.lower() for word in fake.words(1)])} }}}}')
    session_key = factory.LazyFunction(lambda: '_'.join([word.lower() for word in fake.words(2)]))
    ussd_menu = factory.LazyFunction(
        lambda: random.choice(models.UssdMenu.objects.filter(menu_type__name=MENU_SCREEN_NAME)))

    @factory.lazy_attribute
    def with_items(self):
        words1 = [word.lower() for word in fake.words(2)]
        words2 = [word.lower() for word in fake.words(4)]
        return f'{{{{{"_".join(words1)}.{"_".join(words2)}}}}}'


class MenuOptionFactory(DjangoModelFactory):
    class Meta:
        model = models.MenuOption

    menu = factory.LazyFunction(lambda: random.choice(models.UssdMenu.objects.filter(menu_type__name=MENU_SCREEN_NAME)))
    language = factory.LazyFunction(lambda: random.choice(models.Language.objects.all()))
    option_text = factory.LazyFunction(lambda: ' '.join([word.capitalize() for word in fake.words(6)]))
    order = factory.LazyFunction(lambda: random.choice([number for number in range(1, 11)]))
    next_screen = factory.LazyFunction(lambda: random.choice(models.UssdMenu.objects.all()))
    is_active = True


class RouterOptionFactory(DjangoModelFactory):
    class Meta:
        model = models.RouterOption

    menu = factory.LazyFunction(
        lambda: random.choice(models.UssdMenu.objects.filter(menu_type__name=ROUTER_SCREEN_NAME)))
    next_screen = factory.LazyFunction(lambda: random.choice(models.UssdMenu.objects.all()))

    @factory.lazy_attribute
    def menu_expression(self):
        words1 = [word.lower() for word in fake.words(2)]
        words2 = [word.lower() for word in fake.words(4)]
        expression_session_key = f'{"_".join(words1)}.{"_".join(words2)}'
        expression_value = random.choice(['00', '99', '50'])
        expression_operator = random.choice(models.RouterOption.COMPARISON_OPERATORS)
        expression = f'{{{{{expression_session_key}{expression_operator}\'{expression_value}\'}}}}'
        return expression
