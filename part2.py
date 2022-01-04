import random
from typing import Optional

import game_tree
import minichess


def generate_complete_game_tree(root_move: str, game_state: minichess.MinichessGame,
                                d: int) -> game_tree.GameTree:
    """Generate a complete game tree of depth d for all valid moves from the current game_state.

    For the returned GameTree:
        - Its root move is root_move.
        - Its `is_white_move` attribute is set using the current game_state.
        - It contains all possible move sequences of length <= d from game_state.
          For each node in the tree, its subtrees appear in the same order that their
          moves were returned by game_state.get_valid_moves(),
        - If d == 0, a size-one GameTree is returned.

    Note that some paths down the tree may have length < d, because they result in an end state
    (win or draw) from game_state in fewer than d moves.

    Preconditions:
        - d >= 0
        - root_move == GAME_START_MOVE or root_move is a valid chess move
    """
    if game_state.get_winner() == 'White':
        if d == 0:
            tree = game_tree.GameTree(root_move, game_state.is_white_move(), 1.0)
            return tree
        else:
            # tree = game_state.copy_and_make_move(root_move)
            # tree._is_white_active = not tree.is_white_move()
            valid_moves = game_state.get_valid_moves()
            # game_state.is_white_move = not game_state.is_white_move()
            tree = game_tree.GameTree(root_move, game_state.is_white_move(), 1.0)
            for move in valid_moves:
                new_tree = game_state.copy_and_make_move(move)
                tree.add_subtree(generate_complete_game_tree(move, new_tree, d - 1))
            return tree
    else:
        if d == 0:
            tree = game_tree.GameTree(root_move, game_state.is_white_move())
            return tree
        else:
            # tree = game_state.copy_and_make_move(root_move)
            # tree._is_white_active = not tree.is_white_move()
            valid_moves = game_state.get_valid_moves()
            # game_state.is_white_move = not game_state.is_white_move()
            tree = game_tree.GameTree(root_move, game_state.is_white_move())
            for x in valid_moves:
                new_tree = game_state.copy_and_make_move(x)
                tree.add_subtree(generate_complete_game_tree(x, new_tree, d - 1))
            return tree


class GreedyTreePlayer(minichess.Player):
    """A Minichess player that plays greedily based on a given GameTree.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[game_tree.GameTree]

    def __init__(self, game_tree: game_tree.GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        self._game_tree = game_tree

    def make_move(self, game: minichess.MinichessGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        highest_prob = None
        lowest_prob = None
        prob = 0.0
        prob1 = 1.0

        if previous_move is not None and self._game_tree is not None:
            self._game_tree = self._game_tree.find_subtree_by_move(previous_move)

        if self._game_tree is None or self._game_tree.get_subtrees() == []:
            next_move = random.choice(game.get_valid_moves())
            self._game_tree = None
            return next_move
        else:
            if game.is_white_move():
                for subtree in self._game_tree.get_subtrees():
                    if subtree.white_win_probability > prob:
                        prob = subtree.white_win_probability
                        highest_prob = subtree
                if highest_prob is not None:
                    self._game_tree = highest_prob
                    return highest_prob.move
                else:
                    next_subtree = random.choice(self._game_tree.get_subtrees())
                    self._game_tree = next_subtree
                    return next_subtree.move
            else:
                for subtree in self._game_tree.get_subtrees():
                    if subtree.white_win_probability < prob1:
                        prob1 = subtree.white_win_probability
                        lowest_prob = subtree
                if lowest_prob is not None:
                    self._game_tree = lowest_prob
                    return lowest_prob.move
                else:
                    next_subtree = random.choice(self._game_tree.get_subtrees())
                    self._game_tree = next_subtree
                    return next_subtree.move


def part2_runner(d: int, n: int, white_greedy: bool) -> None:
    """Create a complete game tree with the given depth, and run n games where
    one player is a GreedyTreePlayer and the other is a RandomPlayer.

    The GreedyTreePlayer uses the complete game tree with the given depth.
    If white_greedy is True, the White player is the GreedyTreePlayer and Black is a RandomPlayer.
    This is switched when white_greedy is False.

    Precondtions:
        - d >= 0
        - n >= 1
    """
    game = minichess.MinichessGame()
    tree = generate_complete_game_tree('*', game, d)
    if white_greedy:
        black_player = minichess.RandomPlayer()
        white_player = GreedyTreePlayer(tree)
    else:
        black_player = GreedyTreePlayer(tree)
        white_player = minichess.RandomPlayer()

    minichess.run_games(n, white_player, black_player)


if __name__ == '__main__':
    # Sample call to part2_runner (you can change this, just keep it in the main block!)
    part2_runner(5, 50, True)
