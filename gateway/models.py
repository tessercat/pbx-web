""" Gateway app models module. """
from django.db import models
from sofia.models import SofiaProfile


class Gateway(SofiaProfile):
    """ A SofiaProfile gateway with AclAddresses, DidNumbers. """
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    proxy = models.CharField(max_length=50)
    realm = models.CharField(max_length=50)
    # JSON params field?
    # Datetime registered field and listen for events?


class AclAddress(models.Model):
    """ An IP address for a Gateway. """

    class Meta:
        verbose_name = 'ACL address'
        verbose_name_plural = 'ACL addresses'

    address = models.GenericIPAddressField()
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.gateway} - {self.address}'


class DidNumber(models.Model):
    """ A gateway and a unique number. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['number', 'gateway']
            ),
        ]

    name = models.CharField(max_length=15)
    number = models.CharField(max_length=50)
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.gateway} - {self.extension} {self.name}'
