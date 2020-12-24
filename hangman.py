# Problem Set 2, hangman.py
# Name: Alexei Baida
# Collaborators:
# Time spent: 12+ hours

import random
import string

WORDLIST_FILENAME = "words.txt"
GUESSES_INITIAL = 6
WARNINGS_INITIAL = 3
VOWELS = frozenset('aeiou')
HINT_SIGN = '*'
UNKNOWN_LETTER = '_'


class TextStyle:
    """Class for styling text with different colour/font"""
    DEFAULT = '\033[0m'
    YELLOW = '\033[33m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    SWAP_COLOUR = '\033[7m'

    @classmethod
    def yellow(cls, text):
        return cls.YELLOW + text + cls.DEFAULT

    @classmethod
    def bold(cls, text):
        return cls.BOLD + text + cls.DEFAULT

    @classmethod
    def red(cls, text):
        return cls.RED + text + cls.DEFAULT

    @classmethod
    def change_background_font(cls, text):
        return cls.SWAP_COLOUR + text + cls.DEFAULT


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


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
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
    # & means intersection of these 2 sets
    if set(secret_word) == set(secret_word) & set(letters_guessed):
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
            word += letter
        else:
            word += UNKNOWN_LETTER
    return ' '.join(word)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    new_alphabet = []
    for letter in alphabet:
        if letter not in letters_guessed:
            new_alphabet += letter
    return ''.join(new_alphabet)


def victory(guesses: int, secret_word: str):
    """
    guesses: count of guesses left
    secret_word: the word the user is guessing
    returns: string with congratulations and total score
    """
    total_score = guesses * len(set(secret_word))
    print(TextStyle.change_background_font(f'Congratulations! You won, the secret word was - {secret_word}'))
    print(TextStyle.change_background_font(f'Your total score is {total_score}'))


def letter_check(letter: str, guesses: int, warnings: int) -> tuple:
    """
    letter: entered letter by user
    guesses: count of guesses left
    warnings: count of warnings left
    returns: which consist of letter, updated count of guesses, updated count of warnings
    """

    if letter.isalpha() and len(letter) == 1 or letter == HINT_SIGN:
        is_input_incorrect = False
        return letter, guesses, warnings, is_input_incorrect
    else:
        if warnings <= 0:
            guesses -= 1
            if guesses <= 0:
                is_input_incorrect = False
                return letter, guesses, warnings, is_input_incorrect
        else:
            warnings -= 1
        if len(letter) != 1:
            print(TextStyle.yellow(f'You must enter only 1 letter. {warnings} warnings left. {guesses} left.'))
        elif letter.isalpha() is False:
            print(TextStyle.yellow(
                f'You must enter a letter of the Latin alphabet. Not a number or symbol. {warnings} warnings left {guesses} left.'))
        else:
            print(TextStyle.yellow(
                f'Invalid value. Please enter 1 Latin letter. {warnings} warnings left {guesses} left.'))
        is_input_incorrect = True
        return letter, guesses, warnings, is_input_incorrect


def validate_letter(guesses, warnings):
    """
    guesses: count of guesses left
    warnings: count of warnings left
    returns: validated letter
    """
    while 1:
        letter_entered = input('Enter your guess letter: ')
        letter, guesses, warnings, is_input_incorrect = letter_check(letter_entered, guesses, warnings)
        if not is_input_incorrect:
            break
    return letter


def letter_in_word(letter, guesses, letters_guessed):
    """
        letter: entered letter by user
        guesses: count of guesses left
        letters_guessed: list (of letters), which letters have been guessed so far
        returns: count of guesses after manipulations
    """
    if letter.lower() in secret_word or letter == HINT_SIGN:
        print(TextStyle.bold(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}'))
    elif letter.lower() in VOWELS and letter.lower() not in secret_word:
        print(TextStyle.red(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}'))
        guesses -= 2
    else:
        print(TextStyle.red(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}'))
        guesses -= 1
    return guesses


def game_result(guesses, letters_guessed):
    """
    guesses: count of guesses left
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: boolean: True - game ended(win or loss), False - game not ended
    """
    if is_word_guessed(secret_word, letters_guessed):
        return True
    elif guesses <= 0:
        return True
    return False


def welcome_art(secret_word: str):
    """
    secret_word: the word the user is guessing
    """
    print('''
     _   _                                           __   _____ 
    | | | |                                         /  | |  _  |
    | |_| | __ _ _ __   __ _ _ __ ___   __ _ _ __   `| | | |/' |
    |  _  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \   | | |  /| |
    | | | | (_| | | | | (_| | | | | | | (_| | | | | _| |_\ |_/ /
    \_| |_/\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_| \___(_)___/ 
                        __/ |                                   
                       |___/                                    
    ''')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')


def hangman(secret_word, hints=False):
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
    welcome_art(secret_word)

    # start variables
    guesses = GUESSES_INITIAL
    letters_guessed = set()
    warnings = WARNINGS_INITIAL

    # main game cycle
    while 1:
        result = game_result(guesses, letters_guessed)
        if not result:
            # let the user know his resources
            print(f'You have {guesses} guesses left.')
            available = get_available_letters(letters_guessed)
            print(f'Available letters: {available}')

            # validate letter
            letter = validate_letter(guesses, warnings)
            letters_guessed.add(letter.lower())

            # check if user want hint
            if hints and letter == HINT_SIGN:
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))

            # check if letter in the word and make corresponding output
            guesses = letter_in_word(letter, guesses, letters_guessed)
            print('--------------------------------------------')
        else:
            break
    if is_word_guessed(secret_word, letters_guessed):
        victory(guesses, secret_word)
    else:
        print(TextStyle.change_background_font(f'You lost. Guesses exceeded. The secret word was - {secret_word}'))


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            if my_word[i] == other_word[i]:
                continue
            elif my_word[i] == UNKNOWN_LETTER and other_word[i] not in my_word:
                continue
            else:
                return False
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    my_word_new = my_word.replace(' ', '')
    possible_matches = []
    for word in wordlist:
        if match_with_gaps(my_word_new, word):
            possible_matches.append(word)

    if not possible_matches:
        print('No matches founded')
    else:
        print(f"Possible word matches are: {' '.join(possible_matches)}")


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
    hangman(secret_word, hints=True)


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word)