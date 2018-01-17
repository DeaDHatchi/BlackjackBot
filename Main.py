from random import randint, shuffle
from decimal import Decimal, ROUND_HALF_UP


class Player:
    def __init__(self, starting_amount, minimum_bet):
        self.starting_amount = starting_amount
        self.current_amount = self.starting_amount
        self.minimum_bet = minimum_bet
        self.table = None
        self.strategy = Strategy(player=self, minimum_bet=self.minimum_bet)

    def set_table(self, table):
        self.table = table

    def __add__(self, other):
        self.current_amount += other

    def __sub__(self, other):
        self.current_amount -= other


class Dealer:
    def __init__(self, cards):
        self.table = None
        self.cards = cards
        self.count = 0

    def set_table(self, table):
        self.table = table

    def shuffle(self):
        self.count = 0
        shuffle(self.cards)

    @property
    def true_count(self):
        decks_left = Decimal(len(self.cards)/52)
        true_count = Decimal(self.count / decks_left)
        return Decimal(true_count.quantize(Decimal('.1'))) - 1


class Table:
    def __init__(self, player: Player, dealer: Dealer):
        self.player = player
        self.dealer = dealer


class Card:
    def __init__(self, card_number):
        self.cards = {'A': (1, 11),
                      'K': 10,
                      'Q': 10,
                      'J': 10,
                      '10': 10,
                      '9': 9,
                      '8': 8,
                      '7': 7,
                      '6': 6,
                      '5': 5,
                      '4': 4,
                      '3': 3,
                      '2': 2}
        self.card_number = card_number

    @property
    def value(self):
        return self.cards[self.card_number]


class Hand:
    def __init__(self, hand):
        self.hand = hand


class Deck:
    def __init__(self):
        self.cards = [Card('A'),
                      Card('K'),
                      Card('Q'),
                      Card('J'),
                      Card('10'),
                      Card('9'),
                      Card('8'),
                      Card('7'),
                      Card('6'),
                      Card('5'),
                      Card('4'),
                      Card('3'),
                      Card('2')]*4

    def shuffle(self):
        shuffle(self.cards)


class Decks:
    def __init__(self, deck_count):
        self.cards = Deck().cards * deck_count

    def shuffle(self):
        shuffle(self.cards)


class Strategy:
    def __init__(self, player, minimum_bet):
        self.player = player
        self.options = ['Double_down', 'Split', 'Surrender', 'Hit', 'Stand']
        self.minimum_bet = minimum_bet
        self.current_count = 0

    def basic_strategy(self, my_hand: Hand, dealer_card: Card):
        pass


class Main:
    def __init__(self, deck_count=6, starting_amount=10000, minimum_bet=10):
        self.player = Player(starting_amount, minimum_bet)
        self.dealer = Dealer(Decks(deck_count).cards)
        self.table = Table(self.player, self.dealer)
        self.player.set_table(self.table)
        self.dealer.set_table(self.dealer)


if __name__ == '__main__':
    # x = Main()
    x = Dealer(Decks(4).cards)
    x.count = 13
    print(x.true_count)