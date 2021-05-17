""" Call app forms module. """
from django import forms
from intercom.models import CallGroup, OutboundCall


class IntercomCallForm(forms.ModelForm):
    """ Abstract call form. """

    def clean(self):
        """ Validate that the extension is not in use. """
        extension = self.cleaned_data.get('extension')
        action = extension.get_action()
        if action and hasattr(action, 'intercom_action'):
            if action != self.instance:
                raise forms.ValidationError('Extension in use.')
        return self.cleaned_data


class CallGroupForm(IntercomCallForm):
    """ Custom CallGroup form. """
    class Meta:
        model = CallGroup
        fields = ('extension', 'lines')


class OutboundCallForm(IntercomCallForm):
    """ Custom OutboundCall form. """
    class Meta:
        model = OutboundCall
        fields = ('extension', 'phone_number', 'gateway')
