""" Common views module. """
import logging
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.shortcuts import render
from common.apps import common_settings


protected_paths = []


def register_protected_path(path):
    """ Add paths to the global protected paths registry."""
    protected_paths.append(path)
    logging.getLogger('django.server').info('protected %s', path)


def custom400(request, exception):
    """ Custom 400. """
    # pylint: disable=unused-argument
    return HttpResponseBadRequest(render(
        request,
        'common/error.html',
        {
            'css': common_settings.get('css'),
            'message': 'Bad Request',
            'page_title': '400 Bad Request'
        },
    ))


def custom403(request, reason=''):
    """ Custom 403. """
    # pylint: disable=unused-argument
    return HttpResponseForbidden(render(
        request,
        'common/error.html',
        {
            'css': common_settings.get('css'),
            'message': 'Forbidden',
            'page_title': '403 Forbidden'
        },
    ))


def custom404(request, exception):
    """ Custom 404. """
    # pylint: disable=unused-argument
    if hasattr(request, 'custom404') and callable(request.custom404):
        return request.custom404(request)
    return HttpResponseNotFound(render(
        request,
        'common/error.html',
        {
            'css': common_settings.get('css'),
            'message': 'Not Found',
            'title': '404 Not Found'
        },
    ))
