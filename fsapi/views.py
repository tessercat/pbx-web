""" Fsapi app view module. """
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from fsapi.registries import fsapi_handler_registry


def custom404(request):
    """ Custom 404 with 200 status code. """
    return HttpResponse(render(request, 'fsapi/404.xml'))


@method_decorator(csrf_exempt, name='dispatch')
class FsapiView(View):
    """ Process API requests by passing the request to a registered
    fsapi request handler. """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Handle API requests. """
        # pylint: disable=unused-argument
        request.custom404 = custom404
        for handler in fsapi_handler_registry:
            if handler.matches(request):
                template, context = handler.process(request)
                return HttpResponse(render(request, template, context))
        raise Http404
