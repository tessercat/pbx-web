""" Sofia app models module. """
from django.db import models


class SofiaProfile(models.Model):
    """ A generic sofia profile. """
    port = models.IntegerField(
        unique=True
    )
    domain = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.domain.capitalize()


class IntercomProfile(SofiaProfile):
    """ A profile with IntercomLines and Extensions. """


class GatewayProfile(SofiaProfile):
    """ A profile with a gateway, AclAddresses and DidNumbers. """
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    proxy = models.CharField(max_length=50)
    realm = models.CharField(max_length=50)


# IntercomProfile relations

class IntercomLine(models.Model):
    """ A named IntercomProfile username/password registration. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_username',
                fields=['username', 'intercom']
            ),
        ]

    # Validate caller_name as whetever CNAM allows.
    # Autogenerate username/password?

    caller_name = models.CharField(max_length=15)
    username = models.SlugField(
        max_length=50,
    )
    password = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        IntercomProfile,
        on_delete=models.CASCADE
    )
    registered = models.DateTimeField(
        blank=True,
        null=True,
    )
    gateway = models.ForeignKey(
        GatewayProfile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.caller_name


class Extension(models.Model):
    """ An IntercomProfile extension number. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_extension_number',
                fields=['number', 'intercom']
            ),
        ]

    # Validate number as 0-9 only.
    number = models.SlugField(
        max_length=50
    )
    intercom = models.OneToOneField(
        IntercomProfile,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '%s %s' % (self.intercom.domain.capitalize(), self.number)


# GatewayProfile relations

class AclAddress(models.Model):
    """ An IP address for a GatewayProfile. """
    address = models.GenericIPAddressField()
    gateway = models.ForeignKey(
        GatewayProfile,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '%s %s' % (self.gateway.domain.capitalize(), self.address)


class DidNumber(models.Model):
    """ A DID number for a GatewayProfile. """

    class Meta:
        verbose_name = 'DID number'

    number = models.CharField(max_length=50)
    gateway = models.ForeignKey(
        GatewayProfile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '%s %s' % (self.gateway.domain.capitalize(), self.number)
