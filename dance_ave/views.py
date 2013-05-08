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

from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.shortcuts import render, get_object_or_404

from operator import itemgetter, attrgetter

@login_required
def dashboard(request):
    players = [ p for p in m.Player.objects.all() ]
    players = sorted( players, key = attrgetter('completed_stations_count'))
    return render(
            request,
            'dance_ave/dashboard.html',
            {
                'players': players,
            },
            )

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

        session = m.Session.objects.get(identifier=r._sessionId)

        code = r.getValue()
        try:
            song = m.SongStation.objects.get(select_code=code)
        except ObjectDoesNotExist:
            t.say("Sorry, %s is an invalid code!" % code)
            return HttpResponse(t.RenderJson())

        session.player.completed_stations.add(song)

#        try:
#            player = m

        t.say([song.audio_url])
        return HttpResponse(t.RenderJson())
