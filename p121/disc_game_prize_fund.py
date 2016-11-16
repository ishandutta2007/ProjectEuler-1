# disc_game_prize_fund.py
# Game is played in which disc is drawn from bag
# Round 1, bag contains 1 blue, 1 red. Round n, bag contains 1 blue, n red
# Player wins if draws more blues than reds across all rounds
# Calculate maximize winning prize such that house does not incur a loss

import time

#---------------------------------------------------------------------------------
# Recursive function that generates all possibilities of draws and
# calculates probability of winning
# Once a draw set cannot possibly win, its probability is returned as zero
# Blues are represented as 1, reds are 0 for simplicity
def simulate_disc_draws (total_turns, curr_bag = [], curr_prob = 1):
    if len (curr_bag) == total_turns:
        if sum(curr_bag) > total_turns / 2: # winner
            return curr_prob
        return 0   # loser

    # check if already winner
    if sum(curr_bag) > total_turns / 2:
        return curr_prob

    # checking if impossible to draw more blue than red by game's end
    # return zero if so
    max_blue_discs = sum(curr_bag) + (total_turns - len(curr_bag))
    if max_blue_discs <= total_turns / 2:
        return 0

    num_blue_discs = 1
    num_red_discs = len(curr_bag) + 1
    total_prob = 0
        
    disc_choices = [0,1]  # red and blue
    for disc in disc_choices:
        new_bag = curr_bag [:]
        new_prob = curr_prob
        new_bag.append(disc)
        if disc == 1:
            new_prob *= (1.0 * num_blue_discs) / (num_blue_discs + num_red_discs)
        else:
            new_prob *= (1.0 * num_red_discs) / (num_blue_discs + num_red_discs)
        total_prob += simulate_disc_draws (total_turns, new_bag, new_prob)
    return total_prob
#---------------------------------------------------------------------------------

def main():
    start_time = time.time()
    total_turns = 15
    winning_prob = simulate_disc_draws (total_turns)
    min_prize = int(1.0 / winning_prob)
    print min_prize
    print time.time() - start_time
main()
