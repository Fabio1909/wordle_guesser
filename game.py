import sys
from wordle import Wordle
from guesser import Guesser
import argparse
import time
import cProfile


class Game:
    global RESULTS, GUESSES
    GUESSES = [] # number of guesses per game
    RESULTS = [] # was the word guessed?
        
    def score(result, guesses):
        if '-' in result or '+' in result:
            # word was not guessed
            result = False
        else:
            result = True
        RESULTS.append(result)
        if result:
            GUESSES.append(guesses)



    def game(wordle, guesser):
        endgame = False
        guesses = 0
        result = '+++++'
        while not endgame:
            guess = guesser.get_guess(result)
            guesses+=1
            result, endgame = wordle.check_guess(guess)    
            print(result)
        return result, guesses
            
            
    if __name__ == '__main__':
        start_time = time.time() # <--------------- INIZIA IL TEMPO 
        parser = argparse.ArgumentParser()
        parser.add_argument('--r', type=int)
        args = parser.parse_args()
        if args.r:
            successes = []
            wordle = Wordle()
            guesser = Guesser('console')
            for run in range(args.r):
                guesser.restart_game()
                wordle.restart_game()
                results, guesses = game(wordle, guesser)
                score(results, guesses)
            print("You correctly guessed {}% of words. ".format( RESULTS.count(True)/len(RESULTS)*100))
            if GUESSES:
                print("Average number of guesses: ", sum(GUESSES)/len(GUESSES))
                elapsed_time = time.time() - start_time    # <----------- STA ROBA QUI PER FARLO IN MINUTI CARINO
                minutes = elapsed_time // 60
                seconds = elapsed_time % 60
                #Print the runtime in minutes:seconds format
                print(f"Runtime: {int(minutes)} minutes : {seconds:.2f} seconds")
        else:
            # Play manually on console
            guesser = Guesser('manual')
            wordle = Wordle()
            print('Welcome! Let\'s play wordle! ')
            game(wordle, guesser)
        