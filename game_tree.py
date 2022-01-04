from __future__ import annotations

from typing import Optional

GAME_START_MOVE = '*'


class GameTree:
    """A decision tree for Minichess moves.

    Each node in the tree stores a Minichess move and a boolean representing whether
    the current player (who will make the next move) is White or Black.

    Instance Attributes:
      - move: the current chess move (expressed in chess notation), or '*' if this tree
              represents the start of a game
      - is_white_move: True if White is to make the next move after this, False otherwise
      - white_win_probability: represents the probability that white will win from the current
                                game state

    Representation Invariants:
        - self.move == GAME_START_MOVE or self.move is a valid Minichess move
        - self.move != GAME_START_MOVE or self.is_white_move == True
        - 0 <= self.white_win_probability <= 1
    """
    move: str
    is_white_move: bool
    white_win_probability: float

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player

    _subtrees: list[GameTree]

    def __init__(self, move: str = GAME_START_MOVE,
                 is_white_move: bool = True, white_win_probability: float = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments, as illustrated below.

        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        >>> game.is_white_move
        True
        """
        self.move = move
        self.is_white_move = is_white_move
        self._subtrees = []
        self.white_win_probability = white_win_probability

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def find_subtree_by_move(self, move: str) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree

        return None

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""

        self._subtrees.append(subtree)
        self._update_white_win_probability()

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_white_move:
            turn_desc = "White's move"
        else:
            turn_desc = "Black's move"
        move_desc = f'{self.move} -> {turn_desc}\n'
        s = '  ' * depth + move_desc
        if self._subtrees == []:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    ############################################################################
    # Part 1: Loading and "Replaying" Minichess games
    ############################################################################
    def insert_move_sequence(self, moves: list[str], win_probability: float = 0.0) -> None:
        """Insert the given sequence of moves into this tree.

        The inserted moves form a chain of descendants, where:
            - moves[0] is a child of this tree's root
            - moves[1] is a child of moves[0]
            - moves[2] is a child of moves[1]
            - etc.

        Do not create duplicate moves that share the same parent; for example, if moves[0] is
        already a child of this tree's root, you should recurse into that existing subtree rather
        than create a new subtree with moves[0].
        But if moves[0] is not a child of this tree's root, create a new subtree for it
        and append it to the existing list of subtrees.
        """
        moves_copy = moves.copy()
        moves_copy.reverse()
        self.rec_helper(moves_copy, win_probability)

    def rec_helper(self, moves_copy: list, win_probability: float = 0.0) -> None:
        """
        Inserts the subtrees into a given tree
        """
        if moves_copy == []:
            return
        move_tree = self.find_subtree_by_move(moves_copy[-1])

        if move_tree is None:  # this happens when there are no subtrees in the existing tree
            new_subtree = GameTree(moves_copy[-1], not self.is_white_move, win_probability)

            self._subtrees.append(new_subtree)  # add new tree to existing subtrees

            # start process over
            moves_copy.pop()
            new_subtree.rec_helper(moves_copy, win_probability)
            self._update_white_win_probability()
            return
        else:  # if it already exists we want to add the rest of the moves on this list
            # after mutating moves_copy
            moves_copy.pop()
            move_tree.rec_helper(moves_copy, win_probability)
            self._update_white_win_probability()
            return

    ############################################################################
    # Part 2: Complete Game Trees and Win Probabilities
    ############################################################################
    def _update_white_win_probability(self) -> None:
        """Recalculate the white win probability of this tree.

        """
        if self._subtrees == []:
            return
        else:
            if self.is_white_move:
                self.white_win_probability = \
                    max(tree.white_win_probability for tree in self._subtrees)
                return
            else:
                sum_probs = 0
                count = 0

                for subtree in self._subtrees:
                    sum_probs += subtree.white_win_probability
                    count += 1

                self.white_win_probability = sum_probs / count
                return


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
    })
