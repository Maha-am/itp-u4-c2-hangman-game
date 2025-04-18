from .exceptions import *

# Complete with your own, just for fun :)
LIST_OF_WORDS = []

import random
def _get_random_word(list_of_words):
    if not list_of_words:
        raise InvalidListOfWordsException("The list of words is empty.")
    return random.choice(list_of_words)


def _mask_word(word):
    if not word:
        raise InvalidWordException("Invalid word.")
    return '*' * len(word)


def _uncover_word(answer_word, masked_word, character):
    if not answer_word or not masked_word:
        raise InvalidWordException()
    if len(answer_word) != len(masked_word):
        raise InvalidWordException()
    if len(character) != 1:
        raise InvalidGuessedLetterException()

    result = ""
    for aw, mw in zip(answer_word, masked_word):
        if aw.lower() == character.lower():
            result += aw
        else:
            result += mw

    return result


def guess_letter(game, letter):
    if game.get('masked_word') == game.get('answer_word') or game.get('remaining_misses') == 0:
        raise GameFinishedException()

    if letter.lower() in [l.lower() for l in game['previous_guesses']]:
        raise InvalidGuessedLetterException("Letter already guessed.")

    game['previous_guesses'].append(letter.lower())

    if letter.lower() in game['answer_word'].lower():
        new_masked = _uncover_word(game['answer_word'], game['masked_word'], letter)
        game['masked_word'] = new_masked

        if new_masked.lower() == game['answer_word'].lower():
            raise GameWonException()
    else:
        game['remaining_misses'] -= 1
        if game['remaining_misses'] == 0:
            raise GameLostException()

    return game


def start_new_game(list_of_words=None, number_of_guesses=5):
    if list_of_words is None:
        list_of_words = LIST_OF_WORDS

    word_to_guess = _get_random_word(list_of_words)
    masked_word = _mask_word(word_to_guess)
    game = {
        'answer_word': word_to_guess,
        'masked_word': masked_word,
        'previous_guesses': [],
        'remaining_misses': number_of_guesses,
    }

    return game
