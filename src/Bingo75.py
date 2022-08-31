from src.Bingo75UI import Bingo75UI
import random
import time

class Bingo75:

    currentBingoCards = []
    played_numbers = []
    ui_enabled = False
    ui_user_triggered_bingoCard_generation = False
    ui_user_triggered_bingoCard_distribution = False
    ui_user_triggered_start = False
    def __init__(self, N_players, ui_enabled = False):
        if ui_enabled:
            self.ui = Bingo75UI(N_players, self)
    
    def same_cards(self, card1, card2):
        for i in range(len(card1)):
            if (card1[i] != card2[i]):
                return 0
        return 1

    def generate_new_BingoCard(self):
        c = [-1] * 25 
        start = 1
        end = 15
        for icol in range (5):
            for irow in range (5):
                number = random.randint(start, end)
                while number in c[icol*5:icol*5+5]:
                    number = random.randint(start, end)
                c[icol*5+irow] = number
            start += 15
            end +=15
        c[12] = 'X'
        return c

    def add_N_BingoCards(self, n):
        for i in range(n):
            card = self.generate_new_BingoCard()
            while card in self.currentBingoCards:
                card = self.generate_new_BingoCard()
            self.currentBingoCards.append(card)

    def get_currentBingoCards(self):
        return self.currentBingoCards[:]

    def extract_number_from_drum(self):
        start = 1
        end = 75
        number = random.randint(start, end)
        while number in self.played_numbers:
            number = random.randint(start, end)
        self.played_numbers.append(number)
        return number

    '''    
    def start_ui(self):
        self.ui_enabled = True
        self.ui.start()
    '''
    
    def wait_until_user_trigger_bingoCards_generation(self):
        while not self.ui_user_triggered_bingoCard_generation:
            time.sleep(0.1)

    def ui_user_trigger_bingoCards_generation(self):
        self.ui_user_triggered_bingoCard_generation = True

    def wait_until_user_trigger_distribution(self):
        while not self.ui_user_triggered_bingoCard_distribution:
            time.sleep(0.1)

    def ui_user_trigger_bingoCard_distribution(self):
        self.ui_user_triggered_bingoCard_distribution = True

    def wait_until_user_trigger_start(self):
        while not self.ui_user_triggered_start:
            time.sleep(0.1)

    def ui_user_trigger_start(self):
        self.ui_user_triggered_start = True

    def ui_update_new_number(self,n):
        self.ui.ui_view2_updateNewNumber(n)

    def ui_set_winner(self, winner, card=None):
        self.ui.ui_view2_updateWinner(winner=winner,card=card)


