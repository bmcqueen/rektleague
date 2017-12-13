from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from riot_request import RiotRequester
from .models import Player, TeamPlayer, Team, Season
from .forms import TournamentCodeForm

def season_detail(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    teams = Team.objects.filter(season=season_id)
    context = {
        'season': season,
        'teams': teams,
    }
    return render(request, 'stats/season.html', context)

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    team_players = TeamPlayer.objects.filter(player=player_id)
    context = {
        'player': player,
        'team_players': team_players
    }
    return render(request, 'stats/player.html', context)

def team_detail(request, season_id, team_id):
    team = get_object_or_404(Team, id=team_id, season=season_id)
    team_players = TeamPlayer.objects.filter(team=team_id)
    context = {
        'team': team,
        'players': team_players,
    }
    return render(request, 'stats/team.html', context)

def index(request):
    team_list = Team.objects.all()
    context = {
        'team_list': team_list,
    }
    return render(request, 'stats/index.html', context)

def load_match(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    if request.method == 'POST':
        form = TournamentCodeForm(request.POST)
        if form.is_valid():
            match_id_requester = RiotRequester('/lol/match/v3/matches/by-tournament-code/')
            match_id = match_id_requester.request(form.cleaned_data['tournament_code'] + '/ids')
            return HttpResponseRedirect('results/' + str(match_id[0]) + '/')
    else:
        form = TournamentCodeForm()
    context = {
        'season': season,
        'form': form,
    }
    return render(request, 'stats/load_match.html', context)


def match_data_results(request, season_id, match_id):
    match_result_requester = RiotRequester('/lol/match/v3/matches/')
    result = match_result_requester.request(str(match_id))
    context = {
        'result': result
    }
    return render(request, 'stats/match_data_results.html', context)


