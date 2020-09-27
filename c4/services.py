from c4.models import Game, Move
import logging

logger = logging.getLogger(__name__)

class MoveServices:

    @staticmethod
    def get_next_row(column, game_uuid):
        last_move_in_column = Move.objects.filter(game__uuid=game_uuid, column=column).order_by('-row').first()
        if last_move_in_column:
            return last_move_in_column.row + 1
        else:
            return 0

    @staticmethod
    def is_valid(column, row, upcoming_move_sequence_number, player_color):
        errors = {}
        if column > 6:
            errors['column'] = f"column: {column} is not valid, it is greater than 6."
        if column < 0:
            errors['column'] = f"column: {column} is not valid, it is less than 0."

        if row > 5:
            errors['row'] = f"row: {row} is not valid, it is greater than 5."
        if row < 0:
            errors['row'] = f"row: {row} is not valid, it is less than 0."

        if upcoming_move_sequence_number % 2 and player_color == Move.RED:
            errors['player_color'] = f"player_color: {player_color} cannot make move, as it is odd move."

        if not upcoming_move_sequence_number % 2 and player_color == Move.YELLOW:
            errors['player_color'] = f"player_color: {player_color} cannot make move, as it is even move."

        response = {'valid': len(errors)==0, 'errors': errors}

        return response

    @staticmethod
    def make_move(game_uuid, column, row, player_color):
        # TODO: make this function transaction
        game = Game.objects.get(uuid=game_uuid)
        move = Move(
            game_id=game.id,
            column=column,
            row=row,
            player_color=player_color,
            sequence_number=game.upcoming_move_sequence_number
        )
        move.save()
        game.upcoming_move_sequence_number += 1
        game.save()


class GameServices:

    @staticmethod
    def get_game_matrix(game_uuid):
        game_matrix = [[None for i in range(7)] for j in range(6)]
        moves = Move.objects.filter(game__uuid=game_uuid)
        logger.info(f"************{len(moves)}**************")
        for move in moves:
            logger.info(move.__dict__)
            game_matrix[move.row][move.column] = move.player_color
        response = {'game matrix': game_matrix}
        return response

    @staticmethod
    def check_if_ended(game_uuid, player_color, current_move_id):
        pass

    @staticmethod
    def check_game_result(game_uuid):
        response = {'ended': False}
        game = Game.objects.get(uuid=game_uuid)
        if game.winner_color:
            response['ended'] = True
            response['winner_color'] = game.winner_color
        return response


    @staticmethod
    def check_turn(game_uuid):
        game = Game.objects.get(uuid=game_uuid)
        response = {'turn': Move.YELLOW if game.upcoming_move_sequence_number % 2 else Move.RED}
        return response

