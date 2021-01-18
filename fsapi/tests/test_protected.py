""" Protected paths test module. """
from django.conf import settings
from common.tests.base import BaseTestCase


class ProtectedPathsTestCase(BaseTestCase):
    """ Verify protected paths responses. """

    def test_fqdnhost(self):
        """ Assert GET fsapi endpoint from not-localhost returns a
        standard 404. """
        response = self.client.get(
            '/fsapi',
            HTTP_X_FORWARDED_HOST=settings.ALLOWED_HOSTS[0],
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.reason_phrase, 'Not Found')
        self.assertEqual(response.templates[0].name, 'common/error.html')

    def test_localhost(self):
        """ Assert GET fsapi endpoint from localhost returns 405. """
        response = self.client.get(
            '/fsapi',
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 405)
