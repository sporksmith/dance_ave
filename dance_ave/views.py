# Create your views here.

from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from tropo import Tropo, Result, Choices, Session
import dance_ave.models as m
from django.core.exceptions import ObjectDoesNotExist

import logging
log = logging.getLogger('django.dance_ave.models')

class Home(View):
    def get(self, request):
        return HttpResponse("get response")

    def post(self, request):
        log.debug('Root got: %s', request.body.__repr__())

        s = Session(request.body)
        sessionid = s.id
        fromaddress = s.fromaddress['id']
        player, created = m.Player.objects.get_or_create(address=fromaddress)
        s_obj, created = m.Session.objects.get_or_create(
                identifier=sessionid,
                defaults={ 'player': player },
                )
        assert(created or s_obj.player.address == fromaddress)

        t = Tropo()
        t.ask(choices = Choices(value="[4 DIGITS]"), timeout=60, name="digit", say = "Enter song code")
        t.on(event = "continue", next ="/django/dance_ave/playcode")

#        t.say("hello django")
#        t.say(['https://s3.amazonaws.com/dance_ave/Ikea.mp3'])
        return HttpResponse(t.RenderJson())

class PlayCode(View):
    def get(self, request):
        return HttpResponse("get response")

    def post(self, request):
        t = Tropo()
        r = Result(request.body)
        log.debug('PlayCode got: %s', request.body.__repr__())

        code = r.getValue()
        try:
            song = m.SongStation.objects.get(select_code=code)
        except ObjectDoesNotExist:
            t.say("Sorry, %s is an invalid code!" % code)
            return HttpResponse(t.RenderJson())

#        try:
#            player = m

        t.say([song.audio_url])
        return HttpResponse(t.RenderJson())
