
import random

DIE_SIDES = 5
TOTAL_DICE = 6
NUM_REROLLS = 2
INITIAL_HP = 10
VICTORY_PTS_TO_WIN = 20
TOKYO_SLOTS = 1

# next thing to add is to give players +1 VP when they move into Tokyo, and +2 VP when they start their turn in Tokyo (double check the rulebook for this.)


def main():
    """
    This Program will play King of Tokyo (without power cards and energy cubes)
    currently it doesn't have moving into and out of tokyo
    """
    PLAYERS = get_players()

    #the following sets up the dictionary stats that is all players' stats
    #here's the fields: pturn, player_number, HP, VP, in_Tokyo, alive)
    # player list is the list of players ["Player 1", "Player 2", ...].  this is for turn order.
    stats = {}
    player_list = []
    for i in range(PLAYERS):
        player_number = "Player " + str(i+1)
        stats[i] = Player(i, player_number, INITIAL_HP, 0, False, True)
        player_list.append(player_number)

    #pturn is for player turn.  it says who's turn it is.
    pturn = 0

    #fix game_on() below to stop when all but one is dead.
    while game_on(stats):
        if stats[pturn].alive:
            input("Press enter to begin " + player_list[pturn] + "'s turn.")
            print(player_list[pturn] + ", it's your turn. Here are the current stats:")

            print_stats(stats, pturn)
            final_dice = dice_time()
            resolve_dice(pturn, final_dice, stats)
            tokyo_movein(pturn, stats)
            print("--------------------------------------------------------")
        else:
            print(player_list[pturn] + ", you are dead. :( ")
        pturn = (pturn + 1) % PLAYERS

    print("The game is over!")


#this returns True if two or more players live and everyone has less than 20 VPs.
def get_players():
    while True:
        try:
            PLAYERS = int(input("How many players?"))
            return PLAYERS
        except ValueError:
            print("Please enter an integer.")

def game_on(stats):
    for key in stats.keys():
        return (stats[key].victory_check() and two_or_more_live(stats))

def two_or_more_live(stats):
    count_alive = 0
    for key in stats.keys():
        if stats[key].HP > 0:
            count_alive += 1
        elif stats[key].HP <= 0:
            stats[key].alive = False
            stats[key].VP = 0
    if count_alive > 1:
        return True
    elif count_alive == 1:
        for key in stats.keys():
            if stats[key].HP > 0:
                print(stats[key].player_number + " is the winner, because everyone else is dead!")

def print_stats(stats, pturn):
    count_Tokyo = 0
    for key in stats.keys():
        print(stats[key].player_number + " has " + str(stats[key].VP) + " VP and " + str(stats[key].HP) + " HP.")
    for key in stats.keys():
        if stats[key].in_Tokyo == True:
            print(stats[key].player_number + " is in Tokyo.")
            count_Tokyo += 1
    if count_Tokyo == 0:
        print("No one is in Tokyo.")
        print(stats[pturn].player_number + ", at the end of your turn you will move into Tokyo")
    elif count_Tokyo < TOKYO_SLOTS:
        print("There is at least one empty space in Tokyo.")
        print(stats[pturn].player_number + ", at the end of your turn, you will move into Tokyo.")


"""
This is one player's turn of dice rolls and rerolls.
It returns a list of the player's final dice rolls (strings), either
'I', 'II', 'III', 'HEAL', or 'SMASH'
"""
def dice_time():

    #This makes a list of TOTAL_DICE word die roles (it rolls TOTAL_DICE word dice)
    input("Press enter to roll all " + str(TOTAL_DICE) + " dice." )
    list_of_dice = roll_all_dice()

    #displays your current dice.
    display_dice(list_of_dice)

    #each iteration of the following loop rerolls the selected dice
    for i in range(NUM_REROLLS):
        #asks how many and what dice to reroll and rerolls the requested dice
        list_of_dice = reroll(list_of_dice)
        # displays current dice
        display_dice(list_of_dice)

    return list_of_dice


#This makes a list of TOTAL_DICE word die rolls.
def roll_all_dice():
    my_dice = []
    for i in range(TOTAL_DICE):
        my_dice.append(roll_word_die())
    return my_dice

#asks user which die to reroll, then rerolls the die the user wants to reroll
#the parameter is the existing dice word list, and the return is the rerolled dice list.

def reroll(my_dice):
    """
    #this makes a bug where it rerolls die 6, because it wraps around, I think.  I'm going to take this out for now.
    #I think I need to do something like this but appending to a list so players can press enter several times.
    #also I need to make sure players can reroll dice infinitely.  I think it's okay.
    while True:
        try:
            dice_to_reroll = list(map(int,input("Enter the numbers of the dice you want to reroll, separated by spaces.  Enter 0 when done.").split()))
        except (SyntaxError, ValueError):
            print("Please enter an integer between 0 and 6")
        if all(x not in [0, 1, 2, 3, 4, 5, 6] for x in dice_to_reroll):
            print("Please enter a 0, 1, 2, 3, 4, 5, or 6.")
        elif 0 in dice_to_reroll:
            break
    """

    dice_to_reroll = []
    #I set die = -1 to avoid an error if the user presses enter w/o entering an input
    die=-1
    #If the user does a non-integer input, it will display both error messages, which is annoying...
    while True:
        try:
            die = int(input("Enter the die number(s) to reroll. Enter 0 when done.  "))
        except (SyntaxError, ValueError):
            print("Please enter an integer between 0 and 6.")
        if die not in [0,1,2,3,4,5,6]:
            print("Please enter a 0, 1, 2, 3, 4, 5, or 6.")
        elif die == 0:
            break
        else:
            dice_to_reroll.append(die)


    #this replaces each die the user wanted to reroll with a rerolled word die
    for i in range(len(dice_to_reroll)):
        my_dice[dice_to_reroll[i]-1] = roll_word_die()

    return my_dice


#this function displays your current dice with their indices (from 1-5 for the user's benefit)
#it's input is the current list of dice rolls as strings.  It prints out the list for the user.
def display_dice(list):
    for i in range(len(list)):
        print("Die " + str(i+1) + " is:   " + list[i])


#this function rolls a die with DICE_SIDES sides.
def roll_die():
    die_roll = random.randint(1, DIE_SIDES)
    return die_roll

#this function rolls a die with words on it from King of Tokyo
def roll_word_die():
    die = roll_die()
    if die == 1:
        return "I"
    elif die == 2:
        return "II"
    elif die == 3:
        return "III"
    elif die == 4:
        return "SMASH"
    elif die == 5:
        return "HEAL"
    else:
        return die
    #the last line is for if you want to modify the game for higher dice sides.



#This will eventually resolve the dice, taking as a parameter the list of final dice
#and translates each dice roll into victory points,
#heals, or smashes.  for now, resolve_dice simply prints the effect of heals and smashes.

def resolve_dice(pturn, list_of_dice, stats):

    stats = resolve_heal(pturn, list_of_dice, stats)
    stats = resolve_smash(pturn, list_of_dice, stats)
    stats = resolve_VPs(pturn, list_of_dice, stats)

    return stats

def resolve_VPs(pturn, list_of_dice, stats):
    num_I = list_of_dice.count("I")
    #this resolves the "I" dice
    for i in range(4):
        if num_I == i+3:
            print("+" + str(i+1) + " VP to " + stats[pturn].player_number + "!")
            stats[pturn].VP += i+1

    #this resolves the "II" dice
    num_II = list_of_dice.count("II")
    for i in range(4):
        if num_II == i+3:
            print("+" + str(i+2) + " VP to " + stats[pturn].player_number + "!")
            stats[pturn].VP += i+2
    #this resolves the "III" dice
    num_III = list_of_dice.count("III")
    for i in range(4):
        if num_III == i+3:
            print("+" + str(i+3) + " VP to " + stats[pturn].player_number + "!")
            stats[pturn].VP += i+3

    return stats


def resolve_heal(pturn, list_of_dice, stats):
    start_HP = stats[pturn].HP
    for i in range(list_of_dice.count("HEAL")):
        #adds 1 HP for each heal die to current player's health.
        stats[pturn].HP += 1
    if list_of_dice.count("HEAL") >0 and stats[pturn].HP >= INITIAL_HP:
        stats[pturn].HP = INITIAL_HP
        if INITIAL_HP > start_HP:
            print("+" + str((INITIAL_HP-start_HP)) + " HP!")
    #I want the following to not happen if they max-ed out.  I want to print the difference between their original health and the max health.
    elif list_of_dice.count("HEAL") >0:
        print("+" + str(list_of_dice.count("HEAL")) + " HP!")

    return stats

#the following wounds players in a different Tokyo state than the player.
def resolve_smash(pturn, list_of_dice, stats):
    for i in range(list_of_dice.count("SMASH")):
        for key in stats.keys():
            if stats[key].in_Tokyo != stats[pturn].in_Tokyo:
                stats[key].HP -= 1
            if stats[key].HP <= 0:
                stats[key].alive = False

    if list_of_dice.count("SMASH") >0 and stats[pturn].in_Tokyo == True:
        #make this print the list better.
        print("-" + str(list_of_dice.count("SMASH")) + " HP to everyone outside of Tokyo: " + str([stats[key].player_number for key in stats if stats[key].in_Tokyo == False]))
    elif list_of_dice.count("SMASH") >0 and stats[pturn].in_Tokyo == False:
        print("-" + str(list_of_dice.count("SMASH")) + " HP to anyone in Tokyo: " + str([stats[key].player_number for key in stats if stats[key].in_Tokyo == True]))
        #the people in tokyo need to decide if they want to get out of tokyo.  either or both of them can leave tokyo.
        tokyo_move_out_option(pturn, stats)
    return stats

def tokyo_move_out_option(pturn, stats):
    for player in stats.values():
        if player.in_Tokyo == True:
            print(f"Player {player.player_number}, you have been hit!")
            move_out = False
            while not move_out:
                move_out = input("Would you like to move out of Tokyo?  y/n ")
                if move_out.lower() == ("y" or "yes"):
                    print(f"{player.player_number}, you are moving out of Tokyo.")
                    player.in_Tokyo = False
                elif move_out.lower() == ("n" or "no"):
                    print(f"{player.player_number}, you are staying in Tokyo.  Good luck!")
                else:
                    print("Please enter yes or no.")
                    move_out == False


#this will make the player move into tokyo if no one is in tokyo.
def tokyo_movein(pturn, stats):
    #count how many people in tokyo
    tokyo_count = 0
    for key in stats:
        if stats[key].in_Tokyo == True:
            tokyo_count += 1
    if tokyo_count < TOKYO_SLOTS:
        stats[pturn].in_Tokyo = True
        print(stats[pturn].player_number + ", you move into Tokyo.")


class Player:
    def __init__(self, pturn, player_number, HP, VP, in_Tokyo, alive):
        self.pturn = pturn
        self.player_number = player_number
        self.HP = HP
        self.VP = VP
        self.in_Tokyo = in_Tokyo
        self.alive = alive

    # currently this isn't used, but it will be because players turns should stop when they get to 0 hp.
    def health_check(self):
        if self.HP > 0:
            return True
        else:
            return False

    def victory_check(self):
        if self.VP < VICTORY_PTS_TO_WIN:
            return True
        else:
            print(self.player_number + " has " + str(self.VP) + " Victory Points!")
            print(self.player_number + " wins!")
            return False





# This provided line is required at the end of a Python file
# to call the main() function.
if __name__ == '__main__':
    main()
