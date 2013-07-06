# Create your views here.

from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from tropo import Tropo, Result, Choices, Session, Say
import dance_ave.models as m
from django.core.exceptions import ObjectDoesNotExist

import logging
log = logging.getLogger('django.dance_ave.models')

from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404

from operator import itemgetter, attrgetter

import random
def reset_game():
#    for station in m.SongStation.objects.all():
#        station.select_code = ''.join([ random.choice('0123456789') for x in range(4) ])
#        station.save()

    m.Player.objects.all().delete()

@login_required
def dashboard(request):
    if request.method == 'POST' and request.POST.get('reset_confirm1') and request.POST.get('reset_confirm2'):
        reset_game()
        return HttpResponseRedirect(reverse('dashboard'))

    players = [ p for p in m.Player.objects.all() ]
    players = sorted(
            players,
            key = attrgetter('completed_stations_count'),
            reverse=True,
            )

    stations = m.SongStation.objects.all()
    return render(
            request,
            'dance_ave/dashboard.html',
            {
                'players': players,
                'stations': stations,
            },
            )

def prompt_player(t, player):
    # report how many stations to go
    stations_to_go = m.SongStation.objects.count() - player.completed_stations.count()
    t.say("%d stations to go." % stations_to_go)

    # check if player has won
    if stations_to_go == 0:
        if not player.finish_time:
            player.finish_time = now()
            player.save()
        t.say("You win!")

    # play prompt or current song
    if player.current_station:
        say_string = player.current_station.audio_url
    else:
        say_string = "Enter song code"
    t.ask(choices = Choices(value="[4 DIGITS]", mode="dtmf"),
            bargein=True,
            timeout=5,
            name="digit",
            say = say_string,
            )
    t.on(event = "continue", next ="/django/dance_ave/playcode")

class Home(View):
    def get(self, request):
        return HttpResponse("get response")

    @method_decorator(csrf_exempt)
    def post(self, request):
        log.debug('Root got: %s', request.body.__repr__())

        s = Session(request.body)
        sessionid = s.id
        fromaddress = s.fromaddress['id']
        player, player_created = m.Player.objects.get_or_create(address=fromaddress)
        s_obj, session_created = m.Session.objects.get_or_create(
                identifier=sessionid,
                defaults={ 'player': player },
                )
        log.info("Player %s started session %s", player, s_obj)

        t = Tropo()
        if player_created:
            t.say("Welcome to Dance Avenue, new player!")
        else:
            t.say("Welcome back to Dance Avenue!")

        prompt_player(t, player)

        tropo_response = t.RenderJson()
        log.debug('Root returning %s', tropo_response)
        return HttpResponse(tropo_response)

class PlayCode(View):
    def get(self, request):
        return HttpResponse("get response")

    @method_decorator(csrf_exempt)
    def post(self, request):
        t = Tropo()
        r = Result(request.body)
        log.debug('PlayCode got: %s', request.body.__repr__())

        session = m.Session.objects.get(identifier=r._sessionId)
        player = session.player

        if r._state == 'DISCONNECTED':
            log.info('player %s disconnected', session.player)
            return HttpResponse(t.RenderJson())
            
        # see if there's a user-entered code
        try:
            code = r.getValue()
        except KeyError:
            t.say("Please try again.")
            code = None

        # if there's a code, try changing the station
        if code:
            try:
                song = m.SongStation.objects.get(select_code=code)
                player.completed_stations.add(song)
                player.current_station = song
                player.save()
            except ObjectDoesNotExist:
                t.say("Sorry, %s is invalid" % code)

        prompt_player(t, player)

        tropo_response = t.RenderJson()
        log.debug('PlayCode returning %s', tropo_response)
        return HttpResponse(tropo_response)
