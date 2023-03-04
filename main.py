# Ian Fletcher
# This is code from the video "Python for Beginners - Full Course [Programming Tutorial]" by the
# YouTube channel freeCodeCamp.org that I practiced as I watched their tutorial

import random as rand


# Card class
class Card:
    # initializes instance of card using suit and rank
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # overrides string to return rank of suit
    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"


# Deck class
class Deck:
    # initializes instance of Deck
    def __init__(self):
        # creates empty list of cards
        self.cards = []
        # creates array of strings for card suits
        suits = ["spades", "clubs", "hearts", "diamonds"]
        # creates array of lists for rank and value of card
        ranks = [
            {"rank": "A", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "J", "value": 10},
            {"rank": "Q", "value": 10},
            {"rank": "K", "value": 10}
                ]
        # for each value of suits and ranks, adds Card value at the end of cards
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    # shuffle function
    def shuffle(self):
        # checks if length of cards is greater than 1 and if so shuffles the deck
        if len(self.cards) > 1:
            rand.shuffle(self.cards)

    # deal function
    def deal(self, number):
        # creates empty array cards_dealt
        cards_dealt = []
        # until i reaches number and if the length of cards is greater than 0, pops card off of cards
        # and adds it to cards_dealt
        for i in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt


# Hand class
class Hand:
    # initializes self and dealer to false
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0;
        self.dealer = dealer

    # adds card_list to end of cards
    def add_card(self, card_list):
        self.cards.extend(card_list)

    # calculates value of hand
    def calculate_value(self):
        # sets value equal to 0
        self.value = 0
        # sets has_ace equal to false
        has_ace = False
        # for every card in cards, sets value of card to card_value and adds card_value to value
        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            # checks if card is an ace
            if card.rank["rank"] == "A":
                has_ace = True
            # checks if has_ace is ture and if the value is greater than 21 in which case the ace = 1
            if has_ace and self.value > 21:
                self.value -= 10

    # gets the value of the hand and returns the value
    def get_value(self):
        self.calculate_value()
        return self.value

    # checks if the hand equals 21
    def is_blackjack(self):
        return self.get_value == 21

    # displays cards
    def display(self, show_dealer_cards=False):
        # prints user or dealer's hand
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        # for every card in the enumerated cards, checks if conditions are met and if so prints either
        # hidden or the value of the card
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_dealer_cards and not self.is_blackjack:
                print("hidden")
            else:
                print(card)
        # if it isn't the dealer's card, prints the value of the hand
        if not self.dealer:
            print("Value:", self.get_value())
        print()


# Game class
class Game:
    # start of play function
    def play(self):
        # sets game_number and games_to_play to 0
        game_number = 0
        games_to_play = 0
        # prompts user to enter number of games while games_to_play is less than or equal to 0
        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except:
                print("You must enter a number.")
        # runs while there are still games to play
        while game_number < games_to_play:
            # increments game_number by 1
            game_number += 1
            # creates a new deck and shuffles it
            deck = Deck()
            deck.shuffle()
            # creates a new player hand and dealer hand
            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            # deals 2 cards to each player
            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))
            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            # displays dealer and player's hands
            player_hand.display()
            dealer_hand.display()

            # checks if there is a winner yet
            if self.check_winner(player_hand, dealer_hand):
                continue

            # creates empty string choice
            choice = ""
            # while the player's hand is less than 21 and the player chooses hit
            while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                # prompts the player to choose to either hit or stand
                choice = input("Please choose 'Hit' or 'Stand' (or H/S): ").lower()
                print()
                # prompts the player to choose to either hit or stand if input isn't valid
                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please choose 'Hit' or 'Stand' (or H/S): ").lower()
                    print()
                # if the player chooses to hit, adds card to player's hand and displays hand
                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()

            # checks if there is a winner yet
            if self.check_winner(player_hand, dealer_hand):
                continue

            # updates player_hand_value and dealer_hand_value
            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            # while the dealer's hand value is less than 17, adds a card to the dealer's hand
            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()
            # displays the dealer's hand
            dealer_hand.display(show_dealer_cards=True)
            # checks if the winner has been found yet
            if self.check_winner(player_hand, dealer_hand):
                continue

            # prints final results
            print("Final Results")
            print("Your hand:", player_hand_value)
            print("Dealer's hand", dealer_hand_value)
            # checks the winner
            self.check_winner(player_hand, dealer_hand, True)

        print("\nThanks for playing!")

    # check winner function
    def check_winner(self, player_hand, dealer_hand, game_over=False):
        # if the game is not over, checks the following win conditions
        if not game_over:
            if player_hand.get_value() > 21:
                print("You busted. Dealer wins!")
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer busted. You win!")
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both players have blackjack! Tie!")
                return True
            elif player_hand.is_blackjack():
                print("You have blackjack. You win!")
                return True
            elif dealer_hand.is_blackjack():
                print("The dealer has blackjack. Dealer wins!")
                return True
        # if the game is over, checks the following conditions
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("You win!")
            elif player_hand.get_value() < dealer_hand.get_value():
                print("Dealer wins!")
            else:
                print("Tie")
            return True
        return False


# creates new game and runs it
g = Game()
g.play()
