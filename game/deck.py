import random
import constants
import time

"""
Contains the game logic for Texas Hold'em poker
"""

class NotEnoughCardsError(Exception):
    """
    Raised when the deck runs out of cards to be dealt
    """

class VeryWeirdDeckError(Exception):
    """
    Raised when something very odd goes wrong with the deck
    """

class NoSuchCardRankError(Exception):
    """
    Raised when a card rank is specified that doesn't exist
    """

class NoSuchCardSuitError(Exception):
    """
    Raised when a card suit is specified that doesn't exist
    """

class Card:
    """
    Represents a single playing card. Useful for working out rankings and
    suchlike
    """

    def __init__(self, rank, suit):
        """
        Creates a new card instance, calculating its prime number value,
        bytecode and so on from the values passed

        The card's bytecode is mapped as follows:

        +--------------------+--------------------+
        |xxxA KQJT 9876 5432 | CDHS rrrr xxpp pppp|
        +--------------------+--------------------+

        """

        # Sanity check the rank and suit before doing anything else
        if rank not in constants.ranks:
            raise NoSuchCardRankError(rank)
        if suit not in constants.suits:
            raise NoSuchCardSuitError(suit)

        self.rank = rank
        self.suit = suit

        # Get the prime number value of this card
        self.pcode = constants.primes[constants.ranks[self.rank]]

        # The bytecode is done with bitwise operators, this
        self.bytecode = (
            constants.byteRanks[constants.ranks[self.rank]] |
            constants.suits[self.suit] |
            (constants.ranks[self.rank] << 8) |
            self.pcode)

    @staticmethod
    def fromByteCode(bytecode):
        """
        Takes a bytecode in (as described for __init__) and creates a Card
        instance for it

        bytecode
            The bytecode from which the Card instance should be generated
        """

        # We can get all the info we need from the second byte of the
        # bytecode.
        info = bytecode & 0x0000FF00

        # The suit is in the leftmost nibble as a flag
        for suit, code in constants.suits.items():
            if info & code:
                cardSuit = suit

        # And we can get the rank from the other nibble
        rankBC = (info >> 8) & 0xF

        # Sanity-check the rank
        if rankBC not in constants.ranks.values():
            raise NoSuchCardRankError("Rank not found:", rankBC)

        keys     = constants.ranks.keys()
        values   = constants.ranks.values()
        rank     = keys[values.index(rankBC)]

        card = Card(rank, cardSuit)
        return card

    def __str__(self):
        return self.rank + ' of ' + self.suit

    def __repr__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self, shuffle = 1):
        """
        Initialises the deck; creates a standard deck of cards, ordered, and
        then uses the shuffle() method to shuffle them into a random order

        shuffle
            Indicates how many times (if any) the deck should be shuffled
            on instantiation
        """
        self.deck = []

        # Build the deck, looping through the suits and adding the
        # appropriate cards
        for suit in constants.suits:
            for rank in constants.ranks:
                # Typecast numeric values into strings
                self.deck.append(Card(rank, suit))

        # We should have fifty two cards, but let's check to be sure
        if len(self.deck) != 52:
            raise VeryWeirdDeckError("Only", len(self.deck), "cards in deck")

        # If requested, shuffle the deck
        for i in range(shuffle):
            self.shuffle()

    def hasCards(self):
        """
        Indicates whether or not there are cards remaining in the deck
        """
        return (len(self.deck) > 0)

    def shuffle(self):
        """
        Shuffles the current deck of cards
        """
        rand = random.Random()
        rand.shuffle(self.deck)

    def deal(self, count = 1):
        """
        Deals a number of cards from the deck.

        count
            The number of cards to deal. If there aren't enough cards in the
            deck, raises a NotEnoughCardsError
        """

        # Check we've got enough cards
        if len(self.deck) < count:
            raise NotEnoughCardsError()

        # If we're only dealing 1 card, do so
        if count is 1:
            return self.deck.pop()

        # If we're dealing more than one card, return a list
        rtn = []
        for i in range(count):
            rtn.append(self.deck.pop())

        return rtn

def deckTest():
    start = time.time()
    players = [[],[],[],[],[],[],[]]
    d = Deck()

    for i in range(2):
        for player in players:
            player.append(d.deal())

    end = time.time()
    print players
    print "That took", str(end - start), "seconds"
