import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.csrf import csrf_exempt


from webargs.djangoparser import use_args
from webargs import fields

from c4.models import Game, Move
from c4.services import MoveServices, GameServices
from c4.middlewares import GameUUIDCheckMiddleware

import logging

logger = logging.getLogger(__name__)

def health_check(request):
    logger.info(request.headers)
    return JsonResponse(data={'status': "app is running"}, status=200)


@csrf_exempt
def start_game(request):
    game = Game()
    game.save()
    data = {'game_uuid': game.uuid}
    return JsonResponse(data=data, status=201)

@csrf_exempt
def make_move(request):
    headers = request.META

    game_uuid = headers.get('HTTP_GAME_UUID', None)
    game = Game.objects.get(uuid=game_uuid)
    data = json.loads(request.body)

    column = data.get('column', None)
    player_color = data.get('player_color', None)

    # TODO: check column and player_color valid

    row = MoveServices.get_next_row(column=column,
                                    game_uuid=game_uuid)

    move_status = MoveServices.is_valid(
        column=column,
        row=row,
        upcoming_move_sequence_number=game.upcoming_move_sequence_number,
        player_color=player_color,
        winner_color=game.winner_color
    )

    if move_status['valid']:
        move_creation_status = MoveServices.make_move(game_uuid, column, row, player_color)
        game_status = GameServices.check_if_ended(
            game_uuid=game_uuid,
            player_color=player_color,
            current_move_id=move_creation_status['move_id']
        )
        response = game_status
        response['move_id'] = move_creation_status['move_id']
        return JsonResponse(data=response, status=201)
    else:
        return JsonResponse(data=move_status, status=409)

    return HttpResponse(content="app is running", status=201)

def show_game_state(request):
    headers = request.META

    game_uuid = headers.get('HTTP_GAME_UUID', None)
    response = GameServices.get_game_matrix(game_uuid)

    return TemplateResponse(
            request, "game_state.html", response
        )
    # return JsonResponse(data=response, status=200)


def check_game_result(request):
    headers = request.META

    game_uuid = headers.get('HTTP_GAME_UUID', None)
    response = GameServices.check_game_result(game_uuid)

    return JsonResponse(data=response, status=200)


def check_turn(request):
    headers = request.META

    game_uuid = headers.get('HTTP_GAME_UUID', None)
    response = GameServices.check_turn(game_uuid)
    return JsonResponse(data=response, status=200)







