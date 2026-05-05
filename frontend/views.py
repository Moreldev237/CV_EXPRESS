from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    """Page d'accueil"""
    return render(request, 'index.html')


def auth(request):
    """Page d'authentification (connexion/inscription)"""
    return render(request, 'auth.html')


@login_required(login_url='/auth')
def dashboard(request):
    """Tableau de bord utilisateur"""
    return render(request, 'dashboard.html', {
        'user': request.user
    })


@login_required(login_url='/auth')
def cv_builder(request):
    """Créateur de CV"""
    return render(request, 'cv-builder.html')


@login_required(login_url='/auth')
def cover_letter(request):
    """Générateur de lettre de motivation"""
    return render(request, 'cover-letter.html')
