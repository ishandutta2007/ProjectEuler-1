# cards.py
# Class for playing cards

import sys
import operator

class Cards:


    rank_dict = {}
    for i in range(2,10):
        rank_dict[str(i)] = i
    rank_dict['T'] = 10
    rank_dict['J'] = 11
    rank_dict['Q'] = 12
    rank_dict['K'] = 13
    rank_dict['A'] = 14

    def __init__ (self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.rank_num = self.rank_dict[rank]
        
        acceptable_suits = ['C', 'D', 'H', 'S']
        acceptable_ranks = ['A', 'K', 'Q', 'J', 'T']
        
        for i in range (2,10):
            acceptable_ranks.append (str(i))

        if suit not in acceptable_suits:
            print "Not acceptable suit"
            sys.exit(0)

        if rank not in acceptable_ranks:
            print rank, "Not acceptable rank"
            sys.exit(0)

    def print_card (self):
        print self.rank

class Hands:

    rank_dict = {}
    for i in range(2,10):
        rank_dict[str(i)] = i
    rank_dict['T'] = 10
    rank_dict['J'] = 11
    rank_dict['Q'] = 12
    rank_dict['K'] = 13
    rank_dict['A'] = 14

    def __init__ (self, card_list):
        num_cards = 5
        if len(card_list) != num_cards:
            print "Incorrect number of cards in hand"
            sys.exit(0)
        self.card_list = card_list
        
        self.card_list.sort (key=operator.attrgetter('rank_num'))

        self.hand_type = self.calc_hand_type()
        
    def print_hand (self):

        for card in self.card_list:
            sys.stdout.write(card.rank + card.suit + ' ')
        sys.stdout.write('\n')
        
    def check_for_straight (self):
        num_cards = 5
        # ranks are sorted in ascending order, so each rank must differ by 1
        for i in range(num_cards-1):
            if self.rank_dict[self.card_list[i+1].rank] - self.rank_dict[self.card_list[i].rank] != 1:
                return 0
        return 1

    def check_for_triple (self):
        num_cards = 5
        # ranks are sorted, so for 3 of a kind, a card and the one after next must be the same
        for i in range(num_cards-2):
            if self.card_list[i+2].rank == self.card_list[i].rank:
                # want to move triple to be last 3 cards of the list
                if i == 0:
                    self.card_list.insert (0, self.card_list.pop(-1))
                    self.card_list.insert (0, self.card_list.pop(-1))

                    # check for full house
                    if self.card_list[0].rank == self.card_list[1].rank:
                        return 2
                    
                if i == 1:  # move last elt before the triple
                    self.card_list.insert (1, self.card_list.pop(-1))                    
                return 1
        return 0

    def check_for_four_kind (self):
        num_cards = 5
        # ranks are sorted, so for 3 of a kind, a card and the one after next must be the same
        for i in range(num_cards-3):
            if self.card_list[i+3].rank == self.card_list[i].rank:
                # Move the singleton to first position in the list
                if i == 0:
                    self.card_list[0], self.card_list[-1] = self.card_list[-1], self.card_list[0]
                return 1
        return 0

    # Assumes we've already checked for 3 of a kind and higher
    def check_pairs (self):
        num_pairs = 0
        pair_beg = []
        for i in range(len(self.card_list)-1):
            if self.card_list[i].rank == self.card_list[i+1].rank:
                num_pairs += 1
                pair_beg.append(i)
        if num_pairs == 0:
            return 0

        if num_pairs == 1 and pair_beg[0] != len(self.card_list)-2: # Move the pair to the end
            self.card_list += [self.card_list.pop(pair_beg[0])]
            self.card_list += [self.card_list.pop(pair_beg[0])]

        if num_pairs == 1:
            return 1
        
        # Want to move singleton to beginning
        if num_pairs == 2:
            if 0 not in pair_beg:
                return 2
            if 2 not in pair_beg:
                self.card_list.insert (0, self.card_list.pop(2))
                return 2
            else:
               self.card_list.insert (0, self.card_list.pop(4))
               return 2
                                
    def check_for_flush (self):
        suit_list = []
        for card in self.card_list:
            suit_list.append (card.suit)
            if len (set(suit_list)) > 1:
                return 0
        return 1
        
    def calc_hand_type (self):

        straight = 0
        flush = 0
        same_card = 0

        straight = self.check_for_straight()
        flush = self.check_for_flush()

        if straight and flush:
            return "Straight flush", 1
        if straight:
            return "Straight", 5
        if flush:
            return "Flush", 4

        if self.check_for_four_kind():
            return "Four of a kind", 2
        if self.check_for_triple() == 2:
            return "Full House", 3
        if self.check_for_triple() == 1:
            return "Three of a kind", 6
        if self.check_pairs() == 2:
            return "Two pair", 7
        if self.check_pairs() == 1:
            return "One pair", 8

        return "High Card", 9

        

