from typing import List, Any, Tuple
from functools import reduce
from random import randrange
from collections import Counter
from math import comb


class Bet:
    """
    Bet of a player
    """

    def __init__(self, count: int = 0, number: int = 0, player: Any = 0):
        match count, number:
            case c, n if c > 0 and n > 0:
                self.dices_count = c
                self.number = n
            case _:
                raise Exception(f'Only positive params are accepted!  {count=} {number=}')
        self.player = player

    def __repr__(self):
        return f"{self.dices_count} {self.number}'s"

class BetFabric:
    """
    Fabric for generating bets with fixed game params
    """

    def __init__(self, max_roll: int = 6, max_dices: int = 5):
        match max_roll, max_dices:
            case r, d if r > 0 and d > 0:
                self.max_roll = max_roll
                self.max_dices_count = max_dices
            case _:
                raise Exception(f'Only positive game config are accepted! {max_roll=} {max_dices=}')

    def get_next_possible_bets(self, bet: Bet) -> List[Bet]:
        if bet.number > self.max_roll or bet.dices_count > self.max_dices_count:
            raise Exception(
                f'invalide bet: {bet.number=} {bet.dices_count=}\n for this game config: {self.max_roll=} {self.max_dices_count}')
        res = []
        for num in range(bet.number + 1, self.max_roll + 1):
            res.append(Bet(self.max_dices_count, num))
        for cnt in range(bet.dices_count + 1, self.max_dices_count + 1):
            for dice in range(1, self.max_roll + 1):
                res.append(Bet(cnt, dice))
        return res

    def get_all_bets(self, player: Any = 0) -> List[Bet]:
        res = []
        for cnt in range(1, self.max_dices_count + 1):
            for dice in range(1, self.max_roll + 1):
                res.append(Bet(cnt, dice, player))
        return res


class Roll:
    """
    Represents simple roll of dices
    """

    def __init__(self, dices_count: int = 5, max_roll: int = 6, dices_list: None | List[int] = None):
        match dices_list:
            case [*dices] if reduce(lambda x, y: x and 0 < y <= max_roll, [True] + dices) and len(dices) == dices_count:
                self.dices = dices
            case [*dices]:
                raise Exception(f'Wrong  {dices=}, also check {dices_count=} and {max_roll=}')
            case _:
                match dices_count, max_roll:
                    case c, m if c > 0 and m > 0:
                        self.dices = [randrange(1, m + 1) for i in range(c)]
                    case _:
                        raise Exception(f'Wrong dice gen params {dices_count=}  {max_roll=}')

    def __repr__(self):
        return f'{self.dices}'


class DeterministicGame:
    """
    Represent one game from perspective of one(!!!) player with history of bets,
    without probabilistic assumptions about the state from bets
    """

    def __init__(self, dices_count_one_player: int = 5, max_roll: int = 6, num_players: int = 2,
                 dices_list: None | List[int] = None):
        match max_roll, dices_count_one_player:
            case r, d if r > 0 and d > 0:
                self.max_roll = max_roll
                self.dices_count_one_player = dices_count_one_player
            case _:
                raise Exception(f'Only positive game config are accepted! {max_roll=} {dices_count_one_player=}')

        self.roll = Roll(dices_count_one_player, max_roll, dices_list)
        self.bet_fabric = BetFabric(max_roll, dices_count_one_player * num_players)
        self.num_players = num_players
        self.bets_history = []

    def estimate_confidence_of_bet(self, bet: Bet) -> float:
        """
        Estimate confidence of a bet, compared to player's state
        """
        # creating Counter each time may be slow, but I don't care now
        dice_counts = Counter(self.roll.dices)
        delta = bet.dices_count - dice_counts[bet.number]
        if delta <= 0:
            # if player has more or equal count of required dices, the bet has 1.0 probability
            return 1.0
        else:
            # maybe different calculation, but it seems ok
            return comb(self.dices_count_one_player * (self.num_players - 1), delta) * ((1 / self.max_roll) ** delta)

    def get_new_bets_with_confidence(self) -> List[Tuple[Bet, float]]:
        bets = []
        if len(self.bets_history) == 0:
            bets = self.bet_fabric.get_all_bets()
        else:
            bets = self.bet_fabric.get_next_possible_bets(self.bets_history[-1])
        confidences = [self.estimate_confidence_of_bet(bet) for bet in bets]
        return sorted(list(zip(bets, confidences)),key=lambda x : x[1], reverse=True)

    def make_bet(self, bet : Bet):
        if bet.dices_count > self.dices_count_one_player * self.num_players:
            raise Exception(f'too much dices in Bet {bet.dices_count=} in the game {self.dices_count_one_player=}')
        if bet.number > self.max_roll:
            raise Exception(f'too big roll for this game {self.max_roll=}')
        self.bets_history.append(bet)



if __name__ == '__main__':
    game = DeterministicGame()
    first_bets = game.get_new_bets_with_confidence()
    game.make_bet(first_bets[0][0])
    second_bets = game.get_new_bets_with_confidence()
    print(first_bets)
    print(second_bets)
    print(game.roll)
