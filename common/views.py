""" Common views module. """
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.shortcuts import render


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
