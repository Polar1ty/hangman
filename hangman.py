# Problem Set 2, hangman.py
# Name: Alexei Baida
# Collaborators:
# Time spent: 5 - 6 hours

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    if set(secret_word) == set(secret_word) & set(letters_guessed):  # & means intersection of these 2 sets
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word = []
    for letter in secret_word:
        if letter in letters_guessed:
            word += f'{letter} '
        else:
            word += '_ '
    return ''.join(word)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    new_alphabet = []
    for letter in alphabet:
        if letter in letters_guessed:
            new_alphabet += ''
        else:
            new_alphabet += f'{letter}'

    return ''.join(new_alphabet)


def victory(guesses, secret_word):
    """
    guesses: count of guesses left
    secret_word: string, the word the user is guessing
    returns: string with congratulations and total score
    """
    total_score = guesses * len(set(secret_word))
    return f'\033[7mCongratulations! You won, the secret word was - {secret_word}\033[0m\n\033[7mYour total score is {total_score}\033[0m'


def letter_check(guesses, warnings):
    """
    guesses: count of guesses left
    warnings: count of warnings left
    returns: confirmed letter
    """
    while 1:
        letter = input('Enter your guess letter:   ')
        if letter.isalpha():
            break
        else:
            if warnings <= 0:
                guesses -= 1
                if guesses == 0:
                    break
            else:
                warnings -= 1
            print(
                f'\033[31mYou must enter a letter of the Latin alphabet. Not a number or symbol. {warnings} warnings left\033[0m')
        print(f'WARNINGS: {warnings}, GUESSES: {guesses}')
    return letter


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print('''
    __  __                                           ___ ____ 
   / / / /___ _____  ____ _____ ___  ____ _____     <  // __ \\
  / /_/ / __ `/ __ \/ __ `/ __ `__ \/ __ `/ __ \    / // / / /
 / __  / /_/ / / / / /_/ / / / / / / /_/ / / / /   / // /_/ / 
/_/ /_/\__,_/_/ /_/\__, /_/ /_/ /_/\__,_/_/ /_/   /_(_)____/  
                  /____/                                      
''')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    guesses = 6
    letters_guessed = []
    vowels = ('a', 'e', 'i', 'o', 'u')
    warnings = 3
    while 1:
        if is_word_guessed(secret_word, letters_guessed):
            print(victory(guesses, secret_word))
            break
        elif guesses <= 0:
            print(f'\033[7mYou lost. Guesses exceeded. The secret word was - {secret_word}\033[0m')
            break
        else:
            print(get_guessed_word(secret_word, letters_guessed))
            print(f'You have {guesses} guesses left.')
            available = get_available_letters(letters_guessed)
            print(f'Available letters: {available}')
            # letter = letter_check(guesses, warnings)
            while 1:
                letter = input('Enter your guess letter:   ')
                if letter.isalpha():
                    break
                else:
                    if warnings <= 0:
                        guesses -= 1
                        if guesses == 0:
                            break
                    else:
                        warnings -= 1
                    print(f'\033[31mYou must enter a letter of the Latin alphabet. Not a number or symbol. {warnings} warnings left\033[0m')
            letters_guessed.append(letter.lower())
            if letter.lower() in secret_word:
                print('\033[1mRight guess!\033[0m')
            elif letter.lower() in vowels and letter.lower() not in secret_word:
                print('\033[1mWrong guess(\033[0m')
                guesses -= 2
            else:
                print('\033[1mWrong guess(\033[0m')
                guesses -= 1
            print('--------------------------------------------')


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

# secret_word = choose_word(wordlist)
# hangman_with_hints(secret_word)
