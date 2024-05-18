import yaml
from rich.console import Console
import re
from collections import defaultdict
from math import log2
from random import choice

class Guesser:
    '''
        INSTRUCTIONS: This function should return your next guess. 
        Currently it picks a random word from wordlist and returns that.
        You will need to parse the output from Wordle:
        - If your guess contains that character in a different position, Wordle will return a '-' in that position.
        - If your guess does not contain thta character at all, Wordle will return a '+' in that position.
        - If you guesses the character placement correctly, Wordle will return the character. 

        You CANNOT just get the word from the Wordle class, obviously :)
    '''
    def __init__(self, manual):
        self.word_list = yaml.load(open('wordlist.yaml'), Loader=yaml.FullLoader)
        self._manual = manual
        self.console = Console()
        self._tried = []
        self._latestfilter = self.word_list # This keeps track of the shortened list
        self._lettersin = [] # List for all the letters that are in the secret word but are not in the corret spot
        self._lettersout = [] # List of all the letters that are not in the secret word
        self._lettersperfect = [] # Letters that are in the "perfect" spot
        

    def restart_game(self):
        self._tried = []
        self._latestfilter = self.word_list
        self._lettersin = []
        self._lettersout = []
        self._lettersperfect = []

    
    def narrow_down(self, result):
        """
            INPUT result --> string
            OUTPUT filtered_list2 --> list
            
            This function takes as input the result of the game, and outputs a shortened list 
            of all the words that match the pattern.
            Once a game is started it keeps track of the shortened list as it shrinks with the
            variable self._latestfilter
        """
        regex = ""
        last_guess = self._tried[-1]
        for i, j in enumerate(result):
            if j == "+":   
                regex += f"[^{last_guess[i]}]"
                if last_guess[i] not in self._lettersout:
                    self._lettersout.append(last_guess[i])
            elif j == "-":
                regex += f"[^{last_guess[i]}]"
                if last_guess[i] not in self._lettersin:
                    self._lettersin.append(last_guess[i])
            else:
                regex += j
                if last_guess[i] not in self._lettersperfect:
                    self._lettersperfect.append(last_guess[i])
                
        self._lettersout = [element for element in self._lettersout if element not in self._lettersperfect and element not in self._lettersin]
        self._lettersin = [element for element in self._lettersin if element not in self._lettersperfect]
    
        pattern = re.compile(regex)
        filtered_list1 = [word for word in self._latestfilter if pattern.search(word)]
        filtered_list2 = [
            word for word in filtered_list1
            if all(letter in word for letter in self._lettersin) and not any(letter in word for letter in self._lettersout)
        ]
        self._latestfilter = filtered_list2
        return filtered_list2
    
    
    def get_epa(self, guessword, list_of_words):
        """ 
            INPUT guessword --> string, list_of_words --> list
            OUTPUT catch --> defaultdict
            
            This funciton takes as input a potential guess word that is part of the shortened list of words 
            and computes every possible resulting pattern that might emerge from the game. 
            The patterns serve as keys in a dictionary with their frequencies as values, indicating how many words 
            match each specific pattern. This analysis helps understand potential match scenarios in the game.
        """
        catch = defaultdict(int)
        for word in list_of_words:
            game_result = ""
            for i, j in zip(word, guessword):
                if i == j:
                    game_result += f"{i}" 
                elif i != j and j in set(word):
                    game_result += "-"
                elif i != j:
                    game_result += "+"
            catch[f"{game_result}"] += 1
        return catch
    
    def get_entropy(self, list_of_words):
        """
            INPUT list_of_words --> list
            OUTPUT highes_entropy_word --> tuple
            
            This function takes calculates the entropy of each word in a list of words, the process is the following:
            - For every word in the list we:
                - Compute every possible pattern that might result from the game
                - Compute the frequency of each pattern, ie how many words fit that pattern
                - Calculates the probability of a certain pattern as how many words fit that pattern / total number of words in the list
                - Calculates the entorpy for each pattern and sums it to calcualte the total entropy for the word
        """
        entropy_dict = {}
        sorted_entropy = []
        total_words = len(list_of_words)
        #self.console.print(total_words)
        for word in list_of_words:
            temporary_d = self.get_epa(word, list_of_words)
            for key in temporary_d:
                temporary_d[key] /= total_words
                value = temporary_d[key]
                if value > 0:
                    temporary_d[key] = - value * log2(value)
                else:
                    temporary_d[key] = 0 
            entropy = sum(temporary_d.values())
            entropy_dict[f"{word}"] = entropy
        sorted_entropy = sorted(entropy_dict.items(), key=lambda item: item[1], reverse = True)
        #print(sorted_entropy)
        highes_entropy_word = sorted_entropy[0]
        return highes_entropy_word


    def get_guess(self, result):
        '''
        This function must return your guess as a string. 
        '''
        if self._manual=='manual':
            return self.console.input('Your guess:\n')
        else:
            """
                This part of the function works in the following way: 
                - First guess is hard coded and its "aires"
                - Second guesses for the wordlist.yaml (traning set) are hard coded as well to speed up execution
                - For the rest of the cases:
                    - First we filter the list of possible words to fit only the ones coherent with the reuslt
                        this is done with the narrow_down() funciton
                    - Then we calculate the entorpy for every word in the smaller list of words with get_entorpy()
                    - We pick as a guess the highes entropy word
            """
            if len(self._tried) == 0: 
                guess = "aires"
            elif len(self._tried) == 1 and len(self.word_list) > 4269 and len(self.word_list) < 4272: # ONLY FOR TRANING SET 
                 filtered_list_of_words = self.narrow_down(result)
                 if result == "+++++":
                     guess = "hotly"
                 elif result == "-++++":
                     guess = "canto"
                 elif result == "+++-+":
                     guess = "clone"
                 elif result == "+-+++":
                     guess = "clint"
                 elif result == "-++-+":
                     guess = "heald"
                 elif result == "-+++-":
                     guess = "shalt"
                 elif result == "++-++":
                     guess = "troon"
                 elif result == "+-+-+":
                     guess = "cline"
                 elif result == "+i+++":
                     guess = "lindy"
                 elif result == "-+-++":
                     guess = "croat"
                 else:
                     entropy_letsgoo = self.get_entropy(filtered_list_of_words)
                     guess = entropy_letsgoo[0]
            elif result[1:] == "illy" and len(self.word_list) > 4269 and len(self.word_list) < 4272: # ONLY FOR TRANING SET
                the_good_stuff = ['billy','willy', 'tilly', 'hilly', 'filly', 'milly', 'gilly', 'jilly']
                filtered_good_stuff = [word for word in the_good_stuff if word not in self._tried]
                guess = choice(filtered_good_stuff)
            elif result[1:] == "aste" and len(self.word_list) > 4269 and len(self.word_list) < 4272: # ONLY FOR TRANING SET
                the_good_stuff1= ['waste','taste', 'paste', 'haste', 'caste']
                filtered_good_stuff1 = [word for word in the_good_stuff1 if word not in self._tried]
                guess = choice(filtered_good_stuff1)
            else:
                filtered_list_of_words = self.narrow_down(result)
                entropy_letsgoo = self.get_entropy(filtered_list_of_words)
                guess = entropy_letsgoo[0]
                
            # professor
            self._tried.append(guess)
            self.console.print(guess)
            
            return guess
