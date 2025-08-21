from django.shortcuts import render


def download(request):
    # Path to the downloadable ZIP file (place your game ZIP in static/spaceinvaders/)
    zip_path = '/static/spaceinvaders/space_invaders_game.zip'
    return render(request, 'spaceinvaders/download.html', {'zip_path': zip_path})
