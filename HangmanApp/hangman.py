import string
from random import choice
import art
from django.conf import settings
import os



class wordPicker():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    WORD_LIST = os.path.join(APP_ROOT, "bigwordlist.txt",)
    wordlist = [word.lower().strip() for word in file(WORD_LIST, 'r').readlines()]
    #wordlist = ['bananarama', 'beautious']
    shortlist = []

    def getSecretWord(self):
          for word in self.wordlist:
              if len(word) > 8:
                  self.shortlist.append(word)
          secret_word = list(choice(self.shortlist))
          return secret_word

def createsolvedsofar(secret_word):
    solvedsofar = []
    for letter in secret_word:
        solvedsofar.append("-")
    return solvedsofar

def validguesstest(guess, bad_guesses, solvedsofar):
    validcharacters = string.lowercase
    if len(guess) != 1:
        result = "Invalid"
        return result
    elif guess not in validcharacters:
        result = "Invalid"
        return result
    elif guess in bad_guesses or guess in solvedsofar:
        result = "Duplicate"
    else:
        result = "Valid"
    return result

def incorrectguesses(secret_word, guess, bad_guesses):
  '''A list of letters guessed that are not in the secret word.'''
  if guess not in secret_word:
    bad_guesses.append(guess)
  return bad_guesses

def getArt(bad_guesses):
  return art.art[len(bad_guesses)]

def guessindex(secret_word, guess):
  '''Creates a list of index values where the guess appears'''
  index = 0
  letterpositions = []
  while index < len(secret_word):
    for letter in secret_word:
      if letter == guess:
        letterpositions.append(index)
      index += 1
  return letterpositions

def solve(solvedsofar, guess, letterpositions):
  '''Rewrite the solvedsofar list with the guess in place'''
  for index in letterpositions:
    solvedsofar[index] = guess
  return solvedsofar

def format(uglylist, withSpaces=True):
  '''Convert puzzle into a string for web display'''
  if not withSpaces:
    return ''.join(map(str,uglylist))
  return ' '.join(map(str,uglylist))

def result(secret_word, solvedsofar, bad_guesses):
  '''Has the player won, lost, or not completed the game?'''
  if solvedsofar == secret_word:
    return 'win'
  elif len(bad_guesses) == 7:
    return 'lose'
  else:
    return 'game in progress'






