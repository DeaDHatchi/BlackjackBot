from random import randint, shuffle
from decimal import Decimal, ROUND_HALF_UP


class Player:
    def __init__(self, starting_amount, minimum_bet):
        self.starting_amount = starting_amount
        self.current_amount = self.starting_amount
        self.minimum_bet = minimum_bet
        self._table = None
        self.strategy = Strategy(player=self, minimum_bet=self.minimum_bet)

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, table):
        self._table = table

    @table.deleter
    def table(self):
        del self._table

    def __add__(self, other):
        self.current_amount += other

    def __sub__(self, other):
        self.current_amount -= other


class Dealer:
    def __init__(self, cards):
        self.cards = cards
        self._table = None
        self.players = []

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, table):
        self._table = table

    @table.deleter
    def table(self):
        del self._table

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def deal_hands(self):
        dealer_hand = None
        player_hand = None
        player_hand = self.cards.pop()
        dealer_hand = self.cards.pop()
        dealer_hand.shown_status = False
        player_hand = (player_hand, self.cards.pop())
        dealer_hand = (dealer_hand, self.cards.pop())

    def deal_card(self):
        card = self.cards.pop()
        self.table.calc_count(card)

    def shuffle(self):
        shuffle(self.cards)


class Table:
    def __init__(self, player: Player, dealer: Dealer):
        self.player = player
        self.dealer = dealer
        self.count = 0

    def calc_count(self, card: Card):
        if card.value == (1, 11):
            self.update_count(-1)
        if card.value < 7:
            self.update_count(1)
        if card.value > 9:
            self.update_count(-1)

    def update_count(self, update):
        self.count += update

    def reset_count(self):
        self.count = 0

    @property
    def true_count(self):
        decks_left = Decimal(len(self.dealer.cards) / 52)
        true_count = Decimal(self.count / decks_left)
        return Decimal(true_count.quantize(Decimal('.1'))) - 1


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
        self.shown_status = True

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
        self.options = {'Double_down': 1, 'Split': 2, 'Surrender': 3, 'Hit': 4, 'Stand': 5}
        self.minimum_bet = minimum_bet
        self.current_count = 0

    def basic_strategy(self, my_hand: Hand, dealer_card: Card):
        # Lets deal with Pairs
        pass


class Main:
    def __init__(self, deck_count=6, starting_amount=10000, minimum_bet=10):
        self.player = Player(starting_amount, minimum_bet)
        self.dealer = Dealer(Decks(deck_count).cards)
        self.table = Table(self.player, self.dealer)

    def set_tables(self):
        self.player.table = self.table
        self.dealer.table = self.table

    def add_player(self):
        self.dealer.add_player(self.player)


if __name__ == '__main__':
    x = Main()
    x.set_tables()
    x.add_player()
