from src.Bingo75 import Bingo75
from src.utils import pretty_card
import time
import mpi4py
mpi4py.rc.initialize = False # do not initialize MPI automatically
mpi4py.rc.finalize = False # do not finalize MPI automatically
from mpi4py import MPI # import the 'MPI'

import argparse

def main(args):
    """Main function

    Args:
        args: See -h
    """
    
    comm = MPI.COMM_WORLD
    comm_size = comm.Get_size()
    num_players = comm_size - 1
    rank = comm.Get_rank()

    GUI_ENABLED = args.gui
    WAIT_SECONDS_BETWEEN_EXTRATIONS = args.wait_seconds_between_numbers
    if (rank==0):
        bingo = Bingo75(num_players, ui_enabled = GUI_ENABLED)

        if GUI_ENABLED:
            print("Waiting util user triggers the creation of the bingoCards....")
            # Wait until user generate the Bingo Cards     
            bingo.wait_until_user_trigger_bingoCards_generation()

        bingo.add_N_BingoCards(num_players)
        bingoCards = bingo.get_currentBingoCards()

        # Print the bingo cards generated
        print("Successfully generated %d bingo cards." % len(bingoCards))
        for i in range(len(bingoCards)):
            print("Player %s:\n%s\n---------------------" % (i, pretty_card(bingoCards[i])))

        if GUI_ENABLED:
            print("Waiting util user triggers the distribution of the bingo cards....")
            # Wait until user starts playing the Bingo Cards
            bingo.wait_until_user_trigger_distribution()
                
        # Send the player cards to the players
        print("Master sends the BingoCards to the players (MPI workers)...")
        for w in range(num_players):
            destination = w+1
            comm.send(bingoCards[w], dest=destination, tag=rank)
        print("Master sent the BingoCards to the players (MPI workers).")

        if GUI_ENABLED:
            print("Waiting util user starts the Bingo game....")
            bingo.wait_until_user_trigger_start()
        
        print("Starting the Bingo game...")
        
        winner = 0
        winner_player = -1
        while not winner:
            # Extract number from the drum
            number = bingo.extract_number_from_drum()

            # GUI
            if GUI_ENABLED:
                bingo.ui_update_new_number(number)

            # Send extracted number to players
            for w in range(num_players):
                destination = w+1
                comm.send(number, dest=destination, tag=rank)

            # Check if there is a winner
            for w in range(num_players):
                player = w+1
                player_won = comm.recv(source = player, tag=player)
                if player_won:
                    winner = 1
                    winner_player = player

            # Notify whether there is a winner
            for w in range(num_players):
                destination = w+1
                comm.send(winner, dest=destination, tag=rank)

            # Sleep
            time.sleep(WAIT_SECONDS_BETWEEN_EXTRATIONS)

        print("END OF THE GAME!")
        print("Numbers extracted from the drum:")
        print(bingo.played_numbers)
        print ("The winner is Player %d. CONGRATULATIONS!" % winner_player)

        if GUI_ENABLED:
            bingo.ui_set_winner(winner_player, bingoCards[winner_player-1])

    else:
        # MPI Workers
        
        # Get player card
        myBingoCard = comm.recv(source=0, tag=0)
        print("[rank %s] My bingo card is:\n%s" % ( str(rank), pretty_card(myBingoCard) ) )

        counter = 0
        won = 0
        winner = False
        while not winner:
            # Receive number extracted from the drum
            number = comm.recv(source=0, tag=0)
            if number in myBingoCard:
                counter += 1

            # Notify if winning
            if counter == 24:
                won = 1
            comm.send(won, dest=0, tag=rank)

            # Receive win condition information
            winner = comm.recv(source=0, tag=0)

if (__name__ == '__main__'):

    # Start MPI
    MPI.Init()

    parser = argparse.ArgumentParser()
    parser.add_argument( "--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument("--gui", action="store_true", help="(bool) Activate the Graphical User Interface")
    parser.add_argument("-w", "--wait-seconds-between-numbers", type=int, help="(int) Seconds between taking numbers from the bingo master. Default: 2 seconds", default=2)
    
    args = parser.parse_args()
    main(args)

    # Finalize MPI
    MPI.Finalize()