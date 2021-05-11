""" Call app models module. """
from django.db import models
from action.models import Action
from sofia.models import SipLine


class Call(Action):
    """ A call action. """
    template = 'call/call.xml'
    line = models.OneToOneField(
        SipLine,
        on_delete=models.CASCADE
    )
