import csv
import random
from typing import Optional

import game_tree
import minichess


################################################################################
# Loading Minichess datasets
################################################################################
def load_game_tree(games_file: str) -> game_tree.GameTree:
    """Create a game tree based on games_file.
    """
    tree = game_tree.GameTree()

    with open(games_file) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            tree.insert_move_sequence(row)
    return tree


################################################################################
# Minichess AI that uses a GameTree
################################################################################
class RandomTreePlayer(minichess.Player):
    """A Minichess player that plays randomly based on a given GameTree.

    This player uses a game tree to make moves, descending into the tree as the game is played.
    On its turn:

        1. First it updates its game tree to its subtree corresponding to the move made by
           its opponent. If no subtree is found, its game tree is set to None.
        2. Then, if its game tree is not None, it picks its next move randomly from among
           the subtrees of its game tree, and then reassigns its game tree to that subtree.
           But if its game tree is None or has no subtrees, the player picks its next move randomly,
           and then sets its game tree to None.
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
        if previous_move is not None and self._game_tree is not None:
            self._game_tree = self._game_tree.find_subtree_by_move(previous_move)

        if self._game_tree is None or self._game_tree.get_subtrees() == []:
            next_move = random.choice(game.get_valid_moves())
            self._game_tree = None
            return next_move
        else:
            next_subtree = random.choice(self._game_tree.get_subtrees())
            self._game_tree = next_subtree
            return next_subtree.move


def part1_runner(games_file: str, n: int, black_random: bool) -> None:
    """Create a game tree from the given file, and run n games where White is a RandomTreePlayer.

    The White player is a RandomTreePlayer whose game tree is the one generated from games_file.
    The Black player is a RandomPlayer if black_random is True, otherwise it is a RandomTreePlayer
    using the SAME game tree as White.

    Precondtions:
        - n >= 1
    """
    game = load_game_tree(games_file)
    white_player = RandomTreePlayer(game)
    if black_random:
        black_player = minichess.RandomPlayer()
    else:
        black_player = RandomTreePlayer(game)

    minichess.run_games(n, white_player, black_player)


if __name__ == '__main__':

    # Sample call to part1_runner (you can change this, just keep it in the main block!)
    part1_runner('data/white_wins.csv', 50, True)

