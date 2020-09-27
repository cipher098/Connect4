from django.http import HttpResponse
from c4.models import Game
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class GameUUIDCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        headers = request.META

        game_uuid = headers.get('HTTP_GAME_UUID', None)
        route_path = headers['PATH_INFO']

        if route_path in ['/healthz/', '/start/']:
            response = self.get_response(request)
            return response

        elif game_uuid:
            try:
                game = Game.objects.filter(uuid=game_uuid).first()
            except ValidationError:
                return HttpResponse(f"UUID: {game_uuid}is not valid. Please check and try again.",
                                    status=404)

            if game:
                response = self.get_response(request)
                return response
            else:
                return HttpResponse(f"Game with UUID: {game_uuid} doesn't exist. Please check and try again.", status=404)
        else:
            return HttpResponse("Unauthorized", status=400)
