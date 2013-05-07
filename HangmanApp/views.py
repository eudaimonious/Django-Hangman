# Create your views here.
import hangman
import art
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse


def index(request):
    #Initialize a list of bad guesses
    request.session['bad_guesses'] = []
    #Initialize guess
    #request.session['guess'] = ''
    #Pick a random long word from the text file
    picker = hangman.wordPicker()
    #Assign that word to a session variable
    request.session['secret_word'] = picker.getSecretWord()
    #Create the puzzle blanks that the user will see and fill in
    request.session['solved_so_far'] = hangman.createsolvedsofar(request.session['secret_word'])
    #Format the puzzle blanks
    request.session['puzzle'] = hangman.format(request.session['solved_so_far'])
    #Get the art
    request.session['art'] = art.art[0]
    #Add to a dict so we can pass these to the template
    context = {
              'secret_word': request.session['secret_word'],
              'solved_so_far': request.session['solved_so_far'],
              'art': request.session['art'],
              'puzzle': request.session['puzzle'],
            }
    return render(request, 'index.html', context)

def anotherturn(request):
    #Convert player's guess from unicode and store
    request.session['guess'] = request.POST['guess'].encode('utf8')
    #Add variables a dict so we can pass these to the template
    context = {
          'secret_word': request.session['secret_word'],
          'solved_so_far': request.session['solved_so_far'],
          'guess': request.session['guess'],
          'bad_guesses': request.session['bad_guesses'],
          'art': request.session['art'],
          'puzzle': request.session['puzzle'],
          'incorrect': request.session['incorrect']
        }
    #Check validity of player's guess
    guessIs = hangman.validguesstest(request.session['guess'], request.session['bad_guesses'], request.session['solved_so_far'])
    #If player's guess is not valid...
    if guessIs != "Valid":
    #Have player try again
          context['guessIs'] = guessIs
          return render(request, 'hangman/anotherturn.html', context)
    #Check if guess in secret word. If not, add to list of bad guesses.
    request.session['bad_guesses'] = hangman.incorrectguesses(request.session['secret_word'], request.session['guess'], request.session['bad_guesses'])
    #Format the incorrect guesses
    request.session['incorrect'] = hangman.format(request.session['bad_guesses'])
    #Update the context passed to render
    context['incorrect'] = request.session['incorrect']
    #Get the appropriate art
    request.session['art'] = hangman.getArt(request.session['bad_guesses'])
    #Update the context passed to render
    context['art'] = request.session['art']
    #Find the index values where the guess appears in the secret word
    letterpositions = hangman.guessindex(request.session['secret_word'], request.session['guess'])
    #Update the puzzle blanks with the player's guess
    request.session['solved_so_far'] = hangman.solve(request.session['solved_so_far'], request.session['guess'], letterpositions)
    #Format the puzzle blanks
    request.session['puzzle'] = hangman.format(request.session['solved_so_far'])
    #update the context passed ot render
    context['puzzle'] = request.session['puzzle']
    #Check on the status of the game
    gameStatus = hangman.result(request.session['secret_word'], request.session['solved_so_far'], request.session['bad_guesses'])
    #If the game should end...
    if gameStatus != 'game in progress':
        #Add the result to the dict so we can pass to the template
        context['result'] = gameStatus
        #Return end game template
        return render(request, 'endgame.html', context)
    #Return anotherturn template
    return render(request, 'anotherturn.html', context)

def endgame(request):
    return render(request, 'endgame.html', context)
