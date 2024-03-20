from django import forms

from menus.models import MenuOption, RouterOption


class BaseTabularIsActiveForm(forms.ModelForm):
    def clean(self):
        """
        This is needed because the default validation fails.
        InlineForm is always sending an 'id' field which is a ModelChoiceField.
        That field gets the default qs not the modified one.
        Therefore, objects that are not 'is_active' are not presented in the ModelChoiceField.
        So when you try to updated from non-active to active those is not in the qs and the whole form
        drops.
        So this method is hijacking the original and revalidate the 'id' fields.

        """

        if self.instance._meta.pk.name not in self.errors:
            return super().clean()
        if not self.instance._meta.pk.name in self.fields:
            return super().clean()

        cleaned_data = super().clean()
        cleaned_data[self.instance._meta.pk.name] = self.instance
        del self.errors[self.instance._meta.pk.name]
        self.cleaned_data = cleaned_data
        return cleaned_data


class MenuOptionsInlineForm(BaseTabularIsActiveForm):
    class Meta:
        model = MenuOption
        fields = ('is_active', 'language', 'option_text', 'order', 'next_screen')


class RouterOptionsInlineForm(BaseTabularIsActiveForm):
    class Meta:
        model = RouterOption
        fields = ('is_active', 'menu', 'menu_expression', 'next_screen')
