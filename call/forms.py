""" Call app forms module. """
from django import forms
from call.models import GroupCall, OutboundCall


class ExtensionCallForm(forms.ModelForm):
    """ Abstract call form. """

    def clean(self):
        """ Validate that the extension is not in use. """
        extension = self.cleaned_data.get('extension')
        action = extension.get_action()
        if action and action != self.instance:
            raise forms.ValidationError('Extension in use.')
        return self.cleaned_data


class GroupCallForm(ExtensionCallForm):
    """ Custom GroupCall form. """
    class Meta:
        model = GroupCall
        fields = ('extension', 'lines')


class OutboundCallForm(ExtensionCallForm):
    """ Custom OutboundCall form. """
    class Meta:
        model = OutboundCall
        fields = ('extension', 'number', 'gateway')
