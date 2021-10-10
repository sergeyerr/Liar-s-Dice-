from typing import List, Tuple

from Base.Core import Bet

"""
functions for choosing bet for list of bets with conditional probs
"""

def max_prob_max_size(possible_bets: List[Tuple[Bet, float]]) -> Bet | None:
    """
    chooses best possible bet with max count of dices
    :param possible_bets:
    :return:
    """
    max_prob = max([x[1] for x in possible_bets])
    # no way
    if max_prob == 0:
        return None
    max_bets = [b for b, prob in possible_bets if prob == max_prob]
    max_bets.sort(key=lambda x: x.dices_count, reverse=True)
    return max_bets[0]


def max_prob_min_size(possible_bets: List[Tuple[Bet, float]]) -> Bet | None:
    """
    choose best possible bet with min count of dices
    :param possible_bets:
    :return:
    """
    max_prob = max([x[1] for x in possible_bets])
    # no way
    if max_prob == 0:
        return None
    max_bets = [b for b, prob in possible_bets if prob == max_prob]
    # the only difference from max size here
    max_bets.sort(key=lambda x: x.dices_count)
    return max_bets[0]

def plus_one_bluffer(possible_bets: List[Tuple[Bet, float]]) -> Bet | None:
    """
    for bad first turns. Takes results from max_size_max_prob, then +1 to number of dices in the bet
    :param possible_bets:
    :return:
    """
    tmp = max_prob_max_size(possible_bets)
    if tmp is not None:
        tmp.dices_count += 1
    return tmp


def bluffer(possible_bets: List[Tuple[Bet, float]], what_to_bluff: int = None) -> Bet | None:
    """
    Makes best bet with chosen number.
    What_to_bluff maybe previous results of bluffing, or just most frequent dice in player's roll.
    :param possible_bets:
    :param previous_bluff_res:
    :return:
    """
    if what_to_bluff is None:
        return None
    ok_bets = [(b, prob) for b, prob in possible_bets if b.number == what_to_bluff]
    if len(ok_bets) == 0:
        return None
    ok_bets.sort(key=lambda x: x[1], reverse=True)
    return ok_bets[0][0]