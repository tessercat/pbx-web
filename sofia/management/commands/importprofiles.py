""" Management utility to manage sofia profiles. """
from django.core.management.base import BaseCommand
from django.conf import settings
from sofia.models import IntercomProfile


class Command(BaseCommand):
    """ A command to manage sofia profiles. """

    help = 'Used to manage sofia profiles.'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        """ Manage sofia profiles. """
        changed = False

        # Delete intercom profiles.
        for intercom in IntercomProfile.objects.all():
            if intercom.domain not in settings.INTERCOM_PORTS:
                intercom.delete()
                changed = True

        # Add intercom profiles.
        for domain, port in settings.INTERCOM_PORTS.items():
            intercom, created = IntercomProfile.objects.get_or_create(
                domain=domain, port=port
            )
            if created:
                print('Created intercom profile', intercom)
                changed = True
            elif intercom.port != port:
                intercom.update(port=port)
                intercom.save()
                print('Changed intercom port for', domain, port)
                changed = True

        # Do gateways.

        # Report.
        if changed:
            print('Restart FreeSWITCH or reload mod_sofia')
        else:
            print('No change')
