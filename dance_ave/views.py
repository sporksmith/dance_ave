# Create your views here.

from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

class Home(View):
    def get(self, request):
        return HttpResponse("get response")

    @method_decorator( csrf_exempt )
    def post(self, request):
        return HttpResponse("post response")
