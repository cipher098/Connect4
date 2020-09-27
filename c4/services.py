from c4.models import Game, Move
import logging

logger = logging.getLogger(__name__)

class MoveServices:

    @staticmethod
    def get_next_row(column, game_uuid):
        last_move_in_column = Move.objects.filter(game__uuid=game_uuid, column=column).order_by('row').first()
        if last_move_in_column:
            return last_move_in_column.row - 1
        else:
            return 5

    @staticmethod
    def is_valid(column, row, upcoming_move_sequence_number, player_color, winner_color):
        errors = {}

        if winner_color:
            errors['winner_color'] = f"Game already won by: {winner_color}. Cannot make move."
        if column > 6:
            errors['column'] = f"column: {column} is not valid, it is greater than 6."
        if column < 0:
            errors['column'] = f"column: {column} is not valid, it is less than 0."

        if row > 5:
            errors['row'] = f"row: {row} is not valid, it is greater than 5."
        if row < 0:
            errors['row'] = f"row: {row} is not valid, it is less than 0. So column is filled, cannot make move in this column."

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
        response = {'status': True, 'move_id': move.id}
        return response


class GameServices:

    @staticmethod
    def get_game_matrix(game_uuid):
        game_matrix = [[None for i in range(7)] for j in range(6)]
        moves = Move.objects.filter(game__uuid=game_uuid)
        for move in moves:
            logger.info(move.__dict__)
            game_matrix[move.row][move.column] = move.player_color
        response = {'game_matrix': game_matrix}
        return response

    @staticmethod
    def check_if_ended(game_uuid, player_color, current_move_id):
        game_matrix = GameServices.get_game_matrix(game_uuid)['game_matrix']
        current_move = Move.objects.get(id=current_move_id)
        game_ended = False
        response = {'game_ended': game_ended}
        # Check for winning condition using rows above it.
        if current_move.row >= 3:
            n_moves = 0
            n_moves += game_matrix[current_move.row][current_move.column] == player_color
            n_moves += game_matrix[current_move.row - 1][current_move.column] == player_color
            n_moves += game_matrix[current_move.row - 2][current_move.column] == player_color
            n_moves += game_matrix[current_move.row - 3][current_move.column] == player_color
            if n_moves >= 4:
                game_ended = True

        # Check for winning condition using rows below it.
        if current_move.row <= 2:
            n_moves = 0
            n_moves += game_matrix[current_move.row][current_move.column] == player_color
            n_moves += game_matrix[current_move.row + 1][current_move.column] == player_color
            n_moves += game_matrix[current_move.row + 2][current_move.column] == player_color
            n_moves += game_matrix[current_move.row + 3][current_move.column] == player_color
            if n_moves >= 4:
                game_ended = True

        # Check for winning condition using column right to it.
        if current_move.column <= 4:
            n_moves = 0
            n_moves += game_matrix[current_move.row][current_move.column] == player_color
            n_moves += game_matrix[current_move.row][current_move.column+1] == player_color
            n_moves += game_matrix[current_move.row][current_move.column+2] == player_color
            n_moves += game_matrix[current_move.row][current_move.column+3] == player_color
            if n_moves >= 4:
                game_ended = True

        # Check for winning condition using column left to it.
        if current_move.column >= 3:
            n_moves = 0
            n_moves += game_matrix[current_move.row][current_move.column] == player_color
            n_moves += game_matrix[current_move.row][current_move.column - 1] == player_color
            n_moves += game_matrix[current_move.row][current_move.column - 2] == player_color
            n_moves += game_matrix[current_move.row][current_move.column - 3] == player_color
            if n_moves >= 4:
                game_ended = True

        # Check for winning condition using Top right cells.
        if current_move.column <= 3 and current_move.row >=3:
            n_moves = 0
            n_moves += game_matrix[current_move.row][current_move.column] == player_color
            n_moves += game_matrix[current_move.row-1][current_move.column+1] == player_color
            n_moves += game_matrix[current_move.row-2][current_move.column+2] == player_color
            n_moves += game_matrix[current_move.row-3][current_move.column+3] == player_color
            if n_moves >= 4:
                game_ended = True

        # Check for winning condition using Top left cells.
        if current_move.column >= 3 and current_move.row >= 3:
            n_moves = 0
            n_moves += game_matrix[current_move.row][current_move.column] == player_color
            n_moves += game_matrix[current_move.row - 1][current_move.column - 1] == player_color
            n_moves += game_matrix[current_move.row - 2][current_move.column - 2] == player_color
            n_moves += game_matrix[current_move.row - 3][current_move.column - 3] == player_color
            if n_moves >= 4:
                game_ended = True

        # Check for winning condition using bottom right cells.
        if current_move.column <= 3 and current_move.row <= 2:
            n_moves = 0
            n_moves += game_matrix[current_move.row][current_move.column] == player_color
            n_moves += game_matrix[current_move.row + 1][current_move.column + 1] == player_color
            n_moves += game_matrix[current_move.row + 2][current_move.column + 2] == player_color
            n_moves += game_matrix[current_move.row + 3][current_move.column + 3] == player_color
            if n_moves >= 4:
                game_ended = True

        # Check for winning condition using bottom left cells.
        if current_move.column >= 3 and current_move.row <= 2:
            n_moves = 0
            n_moves += game_matrix[current_move.row][current_move.column] == player_color
            n_moves += game_matrix[current_move.row + 1][current_move.column - 1] == player_color
            n_moves += game_matrix[current_move.row + 2][current_move.column - 2] == player_color
            n_moves += game_matrix[current_move.row + 3][current_move.column - 3] == player_color
            if n_moves >= 4:
                game_ended = True

        if game_ended:
            game = Game.objects.get(uuid=game_uuid)
            game.winner_color = player_color
            game.save()
            response['game_ended'] = game_ended
            response['winner'] = player_color

        return response



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

