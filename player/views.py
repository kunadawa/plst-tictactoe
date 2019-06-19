"""controller logic for player app"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from gameplay.models import Game
from player.models import Invitation
from .forms import InvitationForm

# Create your views here.

def home(request):
    """respond to /home requests"""

    all_my_games = Game.objects.games_for_user(request.user)
    active_games = all_my_games.active()
    invites_received = request.user.invitations_received.all()

    return render(request, "player/home.html",
                  {'games': active_games,
                   'invites_received':invites_received
                  })

@login_required
def new_invitation(request):
    """ show an a invitation form """
    if request.method == 'POST':
        invite = Invitation(from_user=request.user)
        form = InvitationForm(instance=invite, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()
    return render(request, "player/new_invitation_form.html", {'form': form})
    