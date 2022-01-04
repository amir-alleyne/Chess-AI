
import random
from typing import Optional

import game_tree
import minichess


class ExploringPlayer(minichess.Player):
    """A Minichess player that plays greedily some of the time, and randomly some of the time.

    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[game_tree.GameTree]
    _exploration_probability: float

    def __init__(self, game_tree: game_tree.GameTree, exploration_probability: float) -> None:
        """Initialize this player."""
        self._game_tree = game_tree
        self._exploration_probability = exploration_probability

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
            number = random.uniform(0.0, 1.0)
            if number < self._exploration_probability:
                return self.helper_function(game)
            else:  # if p is greater than or equal to self._exploration_probability
                return self.helper_function2(game)

    def helper_function(self, game: minichess.MinichessGame) -> str:
        """
        ...
        """
        next_move = random.choice(game.get_valid_moves())
        subtrees = self._game_tree.get_subtrees()
        if next_move not in [tree.move for tree in subtrees]:
            self._game_tree = None
            return next_move
        else:
            next_subtree = self._game_tree.find_subtree_by_move(next_move)
            self._game_tree = next_subtree
            return next_subtree.move

    def helper_function2(self, game: minichess.MinichessGame) -> str:
        """
        ...
        """
        highest_prob = None
        lowest_prob = None
        prob = 0.0
        prob1 = 1.0
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


def run_learning_algorithm(exploration_probabilities: list[float],
                           show_stats: bool = True) -> game_tree.GameTree:
    """Play a sequence of Minichess games using an ExploringPlayer as the White player.

    This algorithm first initializes an empty GameTree. All ExploringPlayers will use this
    SAME GameTree object, which will be mutated over the course of the algorithm!
    Return this object.

    There are len(exploration_probabilities) games played, where at game i (starting at 0):
        - White is an ExploringPlayer (using the game tree) whose exploration probability
            is equal to exploration_probabilities[i]
        - Black is a RandomPlayer
        - AFTER the game, the move sequence from the game is inserted into the game tree,
          with a white win probability of 1.0 if White won the game, and 0.0 otherwise.

    """
    # Start with a GameTree in the initial state
    game_tre = game_tree.GameTree()

    # Play games using the GreedyRandomPlayer and update the GameTree after each one
    results_so_far = []

    # Write your loop here, according to the description above.
    for i in range(0, len(exploration_probabilities)):
        white_copy = ExploringPlayer(game_tre, exploration_probabilities[i])
        black_copy = minichess.RandomPlayer()

        game = minichess.run_game(white_copy, black_copy)
        results_so_far.append(game[0])

        if game[0] == 'White':
            game_tre.insert_move_sequence(game[1], 1.0)
        else:
            game_tre.insert_move_sequence(game[1], 0.0)

    if show_stats:
        minichess.plot_game_statistics(results_so_far)

    return game_tre


def part3_runner() -> game_tree.GameTree:
    """Run example for Part 3.
    """
    lst = []
    for x in range(0, 700):
        lst.extend([1 - (x * (1 / 700))])

    lst.extend([0.0] * 500)

    return run_learning_algorithm(lst)


if __name__ == '__main__':

    part3_runner()

