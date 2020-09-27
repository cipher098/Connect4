"""connect4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from c4.api import (
    health_check,
    start_game,
    make_move,
    show_game_state,
    check_game_result,
    check_turn
)

urlpatterns = [
    path('healthz/', health_check),
    path('start/', start_game),
    path('make_move/', make_move),
    path('show_game_state/', show_game_state),
    path('check_game_result/', check_game_result),
    path('check_turn/', check_turn),
]
