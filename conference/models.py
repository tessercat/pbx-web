""" Conference app models module. """
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from verto.models import Channel


class Conference(models.Model):
    """ A verto channel and a topic. """

    channel = models.OneToOneField(
        Channel,
        on_delete=models.CASCADE,
        related_name='application',
    )
    # channel.application
    topic = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return str(self.topic)


@receiver(post_delete, sender=Conference)
def post_delete_user(sender, instance, *args, **kwargs):
    """ Delete channel/clients when conferences are deleted. """
    # pylint: disable=unused-argument
    if instance.channel:
        instance.channel.delete()
