# poker_hands.py
# Take 2 poker hands as each line of file input, and determine winning hand
# Return number of times player 1 wins as output

from cards import Cards, Hands

def convert_str_cards (card_str):

    x1 = Cards (card_str[0], card_str[1])
    return x1

# Compares two poker hands, returns 1 if player 1 wins, 0 if not
def compare_hands (hand_1, hand_2):

    P1_hand = hand_1
    P2_hand = hand_2
    
    if P1_hand.hand_type[1] < P2_hand.hand_type[1]: 
        return 1
    if P1_hand.hand_type[1] == P2_hand.hand_type[1]:
        
        for i in range(num_cards-1, -1, -1):
            if (P1_hand.card_list[i].rank_num > P2_hand.card_list[i].rank_num):
                return 1                    
                
            if (P1_hand.card_list[i].rank_num < P2_hand.card_list[i].rank_num):
                return 0
    return 0

num_cards = 5
input_file = "poker.txt"

with open (input_file, 'r') as f:
    P1_count = 0

    for line in f:  # each player's hand on a line
        x1 = line.split(' ')
        string_hand = []
        poker_hand = []
        for card_type in x1:
            string_hand.append(card_type)

        for card_str in string_hand:
            poker_hand.append (convert_str_cards(card_str))

        P1_hand = Hands(poker_hand[:num_cards])
        P2_hand = Hands(poker_hand[num_cards:])

        P1_count += compare_hands (P1_hand, P2_hand)
        
print P1_count

        
        
