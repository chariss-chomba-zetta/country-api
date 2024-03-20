from django.db import models

from menus.settings import CUSTOM_QUIT_SCREEN_NAME_CODE, CUSTOM_QUIT_SCREEN_NAME_PREFIX, DEFAULT_ERROR_MESSAGE, \
    DEFAULT_LANGUAGE_CODE, QUIT_SCREEN_NAME


class BaseModelManager(models.Manager):
    def get_queryset(self):
        """Filters only is active fields by default"""
        qs = super().get_queryset()
        qs = qs.filter(is_active=True)
        return qs

    def get_full_queryset(self):
        """Returns the initial qs"""
        qs = super().get_queryset()
        return qs


class MainMenuBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    objects = BaseModelManager()


class SecondaryMenuBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ShortCode(MainMenuBaseModel):
    institution = models.CharField(max_length=255)
    shortcode = models.CharField(max_length=50)
    country = models.CharField(max_length=2,
                               help_text='ISO 3166-1 alpha-2 country code. '
                                         'REF: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes')

    def __str__(self):
        return self.shortcode


class MenuType(SecondaryMenuBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DfsService(SecondaryMenuBaseModel):
    class MethodChoices(models.TextChoices):
        POST = 'post'
        GET = 'get'
        PUT = 'put'
        DELETE = 'delete'
        PATCH = 'patch'

    name = models.CharField(max_length=36, unique=True)
    service_function = models.CharField(max_length=255, unique=True)
    url = models.CharField(unique=False, max_length=255)
    method = models.CharField(max_length=10, choices=MethodChoices.choices, default=MethodChoices.POST)
    session_key = models.CharField(max_length=255, blank=True, null=True)
    service_degradation_key = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.name} : {str(self.method)}'


class UssdMenu(MainMenuBaseModel):
    name = models.CharField(max_length=50, help_text='Unique Screen name', unique=True)
    menu_type = models.ForeignKey(MenuType, on_delete=models.CASCADE, related_name='ussd_menu_menu_type',
                                  help_text='Type of the screen')
    shortcode = models.ForeignKey(ShortCode, on_delete=models.CASCADE, related_name='ussd_menu_shortcode',
                                  help_text='Specifies for what dial short code service is this menu for.')
    next_screen = models.ForeignKey(
        to='UssdMenu', blank=True, null=True, related_name='ussd_menu_next_screen', on_delete=models.CASCADE,
        help_text='Specifies the default next screen.'
                  'For [input screens] and [router screens] this is the screen that service will take user to '
                  'if [router options] or [input screen conditions] fail.')
    dfs_service = models.ForeignKey(
        DfsService, on_delete=models.CASCADE, null=True, blank=True, related_name='ussd_menu_dfs_service',
        help_text='Used only on the [function screens] to specify the function that is going to be run on that screen.')
    has_options = models.BooleanField(
        default=False,
        help_text='Used only on the [menu screens] to specify is menu has predefined options or options that are '
                  'iterated through. When checked, predefined options are expected.')
    input_identifier = models.CharField(
        blank=True, max_length=50,
        help_text='Used only on the [input screens] to specify the key in session that '
                  'the user input will be stored under.')

    # input_screen conditional screens
    input_screen_has_back = models.BooleanField(default=True,
                                                help_text='Only used in the "input_screen" screen type. '
                                                          'If marked and input_screen_back_screen is populated, '
                                                          'will take user back to the screen which '
                                                          'input_screen_back_screen refers. /0 option/. '
                                                          'Otherwise, it will lead user to the last visited'
                                                          '"visible screen" in the recorded session.')
    input_screen_back_screen = models.ForeignKey(to='UssdMenu', blank=True, null=True,
                                                 related_name='back_screen',
                                                 on_delete=models.SET_NULL)
    input_screen_has_home = models.BooleanField(default=True, help_text='Only used in the "input_screen" screen type.'
                                                                        'Marks if home /00 option/ is available to '
                                                                        'this screen.')
    input_screen_has_pin_reset = models.BooleanField(default=False,
                                                     help_text='Only used in the "input_screen" screen type.'
                                                               'Marks if reset pin /1 option/ is available '
                                                               'to this screen.')

    # menu_screen conditional screens
    menu_screen_has_back = models.BooleanField(default=True,
                                               help_text='Only used in the "menu_screen" screen type. '
                                                         'If marked and menu_screen_back_screen is populated, '
                                                         'will take user back to the screen which '
                                                         'menu_screen_back_screen refers. '
                                                         'Option is added automatically')
    menu_screen_back_screen = models.ForeignKey(to='UssdMenu', blank=True, null=True,
                                                related_name='menu_back_screen',
                                                on_delete=models.SET_NULL)
    menu_screen_has_home = models.BooleanField(default=True, help_text='Only used in the "menu_screen" screen type.'
                                                                       'Marks if home menu option is available '
                                                                       'to this screen.')

    def __str__(self):
        return self.name

    @property
    def custom_error_screen_name(self):
        return self.generate_custom_error_screen_name(shortcode_obj=self.shortcode)

    @staticmethod
    def generate_custom_error_screen_name(shortcode_obj):
        return f'{CUSTOM_QUIT_SCREEN_NAME_PREFIX}_{shortcode_obj.country}_{shortcode_obj.shortcode}'

    @classmethod
    def create_custom_quit_screen(cls, shortcode_obj):
        menu_type_quit = MenuType.objects.filter(name=QUIT_SCREEN_NAME).first()
        if menu_type_quit is None:
            raise RuntimeError(f'No menu type of {QUIT_SCREEN_NAME} found.')
        obj, created = cls.objects.get_or_create(
            shortcode=shortcode_obj,
            name=cls.generate_custom_error_screen_name(shortcode_obj=shortcode_obj),
            menu_type=menu_type_quit,
            is_active=True,
        )
        default_lang = Language.objects.get(language_code=DEFAULT_LANGUAGE_CODE)
        UssdLabel.objects.get_or_create(menu=obj, language=default_lang, label_text=DEFAULT_ERROR_MESSAGE)
        return obj

    def has_conditional_input_screens(self):
        total_check = self.input_screen_has_back or self.input_screen_has_pin_reset or self.input_screen_has_home
        return total_check

    def has_conditional_menu_screens(self):
        total_check = self.menu_screen_has_back or self.menu_screen_has_home
        return total_check


class Language(MainMenuBaseModel):
    language_code = models.CharField(
        max_length=2,
        help_text='ISO 639-1: two-letter code, lowercase. REF: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes')
    language_name = models.CharField(
        max_length=50, help_text='ISO language name. REF: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes')

    def __str__(self):
        return self.language_name


class NavigationLabel(SecondaryMenuBaseModel):
    """
    Used to hold information about labelling translation
    """

    language = models.OneToOneField(Language, on_delete=models.CASCADE, related_name='navigation_label')
    back_label = models.CharField(
        max_length=25,
        help_text='Used to specify the "BACK" for input screens and menu screens for selected language.'
                  'Do not add prefix - will be added automatically.')
    main_menu_label = models.CharField(
        max_length=25,
        help_text='Used to specify the "MAIN MENU" for input screens and menu screens for selected language.'
                  'Do not add prefix - will be added automatically.')
    pin_reset_label = models.CharField(
        max_length=25,
        help_text='Used to specify the "PIN RESET" flow for the conditional input menus for selected language.'
                  'Do not add prefix - will be added automatically.')

    def __str__(self):
        return f'Navigation labels for {str(self.language)}'


class ErrorLabel(SecondaryMenuBaseModel):
    language = models.OneToOneField(Language, on_delete=models.CASCADE, related_name='conditional_input_words')
    error_message = models.CharField(
        max_length=150,
        help_text='Defines the error message for that language, which will be shown when user do a wrong input.')

    def __str__(self):
        return f'Error label for {str(self.language)}'


class UssdLabel(SecondaryMenuBaseModel):
    menu = models.ForeignKey(to=UssdMenu, on_delete=models.CASCADE, related_name='label_parent_screen')
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE)
    label_text = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.label_text

    class Meta:
        unique_together = ['menu', 'language']


class MenuItem(SecondaryMenuBaseModel):
    item_text = models.CharField(max_length=512)
    item_value = models.CharField(max_length=512)
    with_items = models.CharField(max_length=512)
    session_key = models.CharField(max_length=512)
    ussd_menu = models.ForeignKey(to=UssdMenu, related_name='menu_item_parent_screen', on_delete=models.CASCADE)

    def __str__(self):
        return self.item_text


class MenuOption(MainMenuBaseModel):
    menu = models.ForeignKey(to=UssdMenu, on_delete=models.CASCADE, related_name='menu_option_parent_screen')
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField()
    next_screen = models.ForeignKey(to=UssdMenu, related_name='menu_option_next_screen', on_delete=models.CASCADE)

    def __str__(self):
        return self.option_text

    class Meta:
        ordering = ['order']


class RouterOption(MainMenuBaseModel):
    menu = models.ForeignKey(to=UssdMenu, on_delete=models.CASCADE, related_name='router_option_parent_screen')
    menu_expression = models.CharField(max_length=1024)
    next_screen = models.ForeignKey(to=UssdMenu, related_name='router_option_next_screen', on_delete=models.CASCADE)

    # a list of all values that could be used in menu_expression to compare values
    COMPARISON_OPERATORS = ['==', '!=', '>', '<', '<=', '>=']
    _selected_comparison_operator = None

    def __str__(self):
        return self.menu_expression

    @property
    def menu_expression_comparison_operator(self):
        if self._selected_comparison_operator is not None:
            return self._selected_comparison_operator
        for item in self.COMPARISON_OPERATORS:
            if item in self.menu_expression:
                self._selected_comparison_operator = item
        return self._selected_comparison_operator

    @property
    def menu_expression_session_key(self):
        """
            Extracts the session key /left comparison value/ that is used
            when forming the JINJA2 comparison operation as specified in < menu_expression >.
            Dot notation is used.
        """
        if self.menu_expression_comparison_operator is None:
            return None
        key = self.menu_expression.split(self.menu_expression_comparison_operator)[0].replace('{{', '').strip()
        return key

    @property
    def menu_expression_value(self):
        """
            Extracts the value that session key is compared against /right comparison value/
            in the JINJA2 comparison operation as specified in < menu_expression > .
       """
        if self.menu_expression_comparison_operator is None:
            return None
        value = self.menu_expression.split(self.menu_expression_comparison_operator)[-1].replace('}}', '')
        value = value.replace('\'', '').replace('"', '').strip()
        return value

    def generate_custom_quit_screen_expression(self):
        router_expression = f'{{{{{self.menu_expression_session_key}{self.menu_expression_comparison_operator}' \
                            f'\'{CUSTOM_QUIT_SCREEN_NAME_CODE}\'}}}}'
        return router_expression
