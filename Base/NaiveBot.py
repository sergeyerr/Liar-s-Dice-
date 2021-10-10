from SimpleHeuristics import *
from Base.Core import DeterministicGame
from random import random
from collections import Counter

class NaiveBot:
    """
    from http://web.stanford.edu/class/archive/cs/cs221/cs221.1192/2018/restricted/posters/dyl/poster.pdf
    """
    def __init__(self, threshold: float, bluff_p: float):
        self.bluf_number = None
        self.threshold = threshold
        self.p = bluff_p

    def MakeFirstTurn(self, possible_bets: List[Tuple[Bet, float]]) -> Bet:
        if random() < self.p:
            bet = plus_one_bluffer(possible_bets)
            self.bluf_number = bet.number
            return bet
        else:
            if random() < 0.5:
                return max_prob_max_size(possible_bets)
            else:
                return max_prob_min_size(possible_bets)

    def ReactToBet(self, prev_bet: Tuple[Bet, float], possible_bets: List[Tuple[Bet, float]]) -> Bet | None:
        if prev_bet[1] < self.threshold:
            # end game
            return None
        else:
            rnd = random()
            if rnd < self.p:
                bet = None
                if self.bluf_number is None:
                    # takes previous number as bluff number
                    ### fix
                    bet = bluffer(possible_bets, prev_bet[0].number)
                else:
                    bet = bluffer(possible_bets, self.bluf_number)
                self.bluf_number = bet.number
                return bet
            else:
                rnd = random()
                if rnd < 0.5:
                    return max_prob_max_size(possible_bets)
                else:
                    return max_prob_min_size(possible_bets)


if __name__ == '__main__':

    first = True
    # enter here your dices
    game = DeterministicGame(dices_list=[1,4,5,5,5])
    bot = NaiveBot(0.2, 0.2)
    bet = None
    if first:
        bet = bot.MakeFirstTurn(game.get_new_bets_with_confidence())
        game.make_bet(bet)
        print(bet)
    else:
        bet = -1
    while bet is not None:
        count, number = [int(x) for x in input().split()]
        if count == -1:
            bet = None
            break
        other_bet = Bet(count, number, 1)
        game.make_bet(other_bet)
        prob = game.estimate_confidence_of_bet(other_bet)
        bets = game.get_new_bets_with_confidence()
        bet = bot.ReactToBet((other_bet, prob), bets)
        if bet is None:
            print('LIIEEERRR')
        else:
            print(bet)
            game.make_bet(bet)





