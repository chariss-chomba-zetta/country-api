from django.contrib import admin

from base_app.admin_base import admin_site
from .admin_forms import MenuOptionsInlineForm, RouterOptionsInlineForm
from .models import ErrorLabel, Language, MenuItem, MenuOption, MenuType, NavigationLabel, DfsService, RouterOption, \
    ShortCode, UssdLabel, UssdMenu


class DefaultIsActiveModelAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)

    def get_queryset(self, request):
        # alter default queryset to include all items
        qs = self.model._default_manager.get_full_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_list_display(self, request):
        """Assures that is_active is always displayed in the list"""
        list_display = super().get_list_display(request)
        list_display = (*list_display, 'is_active')
        return list_display

    def get_fields(self, request, obj=None):
        """Always get is_active field in the model admin"""
        fields = super().get_fields(request=request, obj=obj)
        fields = (*fields, 'is_active')
        return fields


class MenuTypesAdmin(admin.ModelAdmin):
    fields = ('name',)


class BaseTabularInline(admin.TabularInline):
    def get_queryset(self, request):
        qs = self.model._default_manager.get_full_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class UssdMenuUssdLabelInline(admin.TabularInline):
    model = UssdLabel
    fk_name = 'menu'
    extra = 1
    can_delete = False


class UssdMenuUssdMenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    can_delete = False


class UssdMenuMenuOptionsInline(BaseTabularInline):
    model = MenuOption
    fk_name = 'menu'
    extra = 1
    can_delete = False
    autocomplete_fields = ['next_screen']
    form = MenuOptionsInlineForm


class UssdMenuRouterOptionsInline(BaseTabularInline):
    model = RouterOption
    fk_name = 'menu'
    extra = 1
    can_delete = False
    autocomplete_fields = ['next_screen']
    form = RouterOptionsInlineForm


class UssdMenuAdmin(DefaultIsActiveModelAdmin):
    fieldsets = (
        ('Base', {
            'fields': (
                'name', 'menu_type', 'is_active', 'shortcode', 'next_screen',
            )
        }),
        ('Screen specific', {
            'fields': (
                'input_identifier', 'dfs_service', 'has_options',
            )
        }),
        ('Conditional Input /only for input screens/', {
            'fields': (
                'input_screen_has_back', 'input_screen_back_screen', 'input_screen_has_home',
                'input_screen_has_pin_reset'
            ),
        }),
        ('Navigation menu options /only for menu screens/', {
            'fields': (
                'menu_screen_has_back', 'menu_screen_back_screen', 'menu_screen_has_home'
            ),
        }),
    )

    search_fields = ['name', 'menu_type__name', 'next_screen__name', 'shortcode__shortcode', 'dfs_service__name',
                     'dfs_service__service_function']
    list_display = ['name', 'shortcode', 'menu_type', 'input_identifier', 'next_screen', 'dfs_service',
                    'shortcode']
    inlines = [
        UssdMenuUssdLabelInline,
        UssdMenuRouterOptionsInline,
        UssdMenuUssdMenuItemInline,
        UssdMenuMenuOptionsInline,
    ]
    autocomplete_fields = ['next_screen', 'input_screen_back_screen', 'menu_screen_back_screen', 'dfs_service']


class LanguageAdmin(DefaultIsActiveModelAdmin):
    fields = ('language_code', 'language_name')


class ShortCodeAdmin(DefaultIsActiveModelAdmin):
    fields = ('institution', 'shortcode', 'country')


class UssdLabelAdmin(admin.ModelAdmin):
    fields = ('menu', 'language', 'label_text')
    search_fields = ['label_text', 'menu__name']
    list_display = ['menu', 'label_text', 'language']
    autocomplete_fields = ['menu']


class DfsServiceAdmin(admin.ModelAdmin):
    fields = ('name', 'service_function', 'url', 'method', 'session_key', 'service_degradation_key')
    list_display = ['name', 'service_function', 'url', 'session_key', 'service_degradation_key']
    search_fields = ['name', 'service_function', 'url', 'session_key', 'service_degradation_key']


class MenuItemsAdmin(admin.ModelAdmin):
    fields = ('ussd_menu', 'item_text', 'item_value', 'with_items', 'session_key',)
    search_fields = ['ussd_menu__name', 'item_text', 'item_value', 'with_items', 'session_key']
    list_display = ['ussd_menu', 'item_text', 'item_value', 'with_items', 'session_key']


class MenuOptionAdmin(DefaultIsActiveModelAdmin):
    fields = ('menu', 'language', 'option_text', 'order', 'next_screen')
    search_fields = ['option_text', 'next_screen__name', 'menu__name']
    list_display = ['option_text', 'menu', 'next_screen', 'language', 'order']


class RouterOptionAdmin(DefaultIsActiveModelAdmin):
    fields = ('menu', 'menu_expression', 'next_screen')
    search_fields = ['menu__name', 'menu_expression', 'next_screen__name']
    list_display = ['menu_expression', 'menu', 'next_screen']


class NavigationLabelAdmin(admin.ModelAdmin):
    fields = ('language', 'back_label', 'main_menu_label', 'pin_reset_label')
    list_display = ['language', 'back_label', 'main_menu_label', 'pin_reset_label']


class ErrorLabelAdmin(admin.ModelAdmin):
    fields = ('language', 'error_message')
    list_display = ['language', 'error_message']


admin_site.register(MenuType, MenuTypesAdmin)
admin_site.register(UssdMenu, UssdMenuAdmin)
admin_site.register(Language, LanguageAdmin)
admin_site.register(NavigationLabel, NavigationLabelAdmin)
admin_site.register(ErrorLabel, ErrorLabelAdmin)
admin_site.register(ShortCode, ShortCodeAdmin)
admin_site.register(UssdLabel, UssdLabelAdmin)
admin_site.register(DfsService, DfsServiceAdmin)
admin_site.register(MenuItem, MenuItemsAdmin)
admin_site.register(MenuOption, MenuOptionAdmin)
admin_site.register(RouterOption, RouterOptionAdmin)
