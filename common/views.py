""" Common views module. """
import os
from markdown import markdown
from django.conf import settings
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from common.decorators import cache_public


def custom400(request, exception):
    """ Custom 400. """
    # pylint: disable=unused-argument
    return HttpResponseBadRequest(render(
        request,
        'common/error.html',
        {'message': 'Bad Request', 'title': '400 Bad Request'},
    ))


def custom403(request, reason=''):
    """ Custom 403. """
    # pylint: disable=unused-argument
    return HttpResponseForbidden(render(
        request,
        'common/error.html',
        {'message': 'Forbidden', 'title': '403 Forbidden'},
    ))


def custom404(request, exception):
    """ Custom 404. """
    # pylint: disable=unused-argument
    if hasattr(request, 'custom404') and callable(request.custom404):
        return request.custom404(request)
    return HttpResponseNotFound(render(
        request,
        'common/error.html',
        {'message': 'Not Found', 'title': '404 Not Found'},
    ))


@method_decorator(cache_public(60 * 15), name='dispatch')
class AboutView(TemplateView):
    """ About the project view. """
    template_name = 'common/about.html'

    def about(self):
        """ Return about page HTML content. """
        # pylint: disable=no-self-use
        path = os.path.join(
            settings.BASE_DIR, 'common', 'markdown', 'about.md',
        )
        with open(path) as about_fd:
            return markdown(about_fd.read())
