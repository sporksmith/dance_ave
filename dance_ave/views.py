# Create your views here.

from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from tropo import Tropo, Result, Choices

class Home(View):
    def get(self, request):
        return HttpResponse("get response")

    def post(self, request):
        t = Tropo()
        t.say("hello django")
        return HttpResponse(t.RenderJson())
