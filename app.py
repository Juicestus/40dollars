#!/usr/bin/env python3

# Main Flask Application (server)
# (c) Justus Languell 2021

#####################
# Include Libraries #
#####################

from flask import (Flask, 
                  render_template, 
                  url_for, 
                  request, 
                  abort, 
                  redirect, 
                  Response, 
                  session)

from flask_socketio import (SocketIO, 
                           emit, 
                           join_room, 
                           leave_room, 
                           close_room, 
                           rooms, 
                           disconnect)

from threading import Timer, Thread

from functools import wraps

import base64
import random
import time
import sys     
import os   

########################
# Initiate Application #
########################

app = Flask(__name__) 
app.secret_key = 'SECRET KEY'
app.config['SECRET_KEY'] = 'SECRET KEY'
socketio = SocketIO(app)        

games = {}

rounds = 4
players = 8

###########
# Prompts #
###########

prompts = [
    "Haydens cock",
    "What to do when stepsis is stuck",
    "What might a person enlarge",
    "Quickest source of femboys",
    "What makes you sad",
    "Where to go to pet furries",
    "The only correct religion",
    "What happened nudiustertian",
    "A person with hircus",
    "Tell me you're a redditor without telling me you're a redditor",
    "Tell me you're a virgin without telling me you're a virgin",
    "How do you cure Pneumonoultramicroscopicsilicovolcanoconiosis",
    "Quickest way to die",
    "Should I kill myself",
    "Reasons to kill oneself",
    "A person sadder than Tadd",
    "A person smarter than Hayden",
    "A person fatter than Grant",
    "A person more cracked at fortnite (my guy) that Jack",
    "Reasons to buy the Gent 65",
    "Types of agriculture",
    "What color is math",
    "Me when I forget to check for extraneous solutions",
    "A rapper Eminem was afraid to dis",
    "Me when it's raining at Taumata­whakatangihanga­koauau­o­tamatea­turi­pukakapiki­maunga­horo­nuku­pokai­whenua­kitanatahu",
    "Next governor of California",
    "Next president of the USA",
    "Somthing that needs to become legal",
    "Something you should never show your grandma",
    "Nastiest food",
    "UFC Fighter Aesthetic",
    "POV Africa",
    "POV You are in Algebra I in 9th grade",
    "POV You have a B in Geometry",
    "POV You're friends with Max",
    "POV Your Gent 65 arives",
    "POV You're the imposter",
    "POV 8 gigs of RAM",
    "POV Vietnam War",
    "POV Jack's new dog",
    "POV Big titty bartender",
    "POV Discord Mod",
    "Scarriest place on Earth",
    "Best kids TV show",
    "Most useful invention ever",
    "What do you do in your spare time",
    "What is your dream job",
    "Something they need to make a LEGO set of",
    "What are we eating",
    "Dream vacation",
    "Something they need to make a sport",
    "Wierdest thing to eat",
    "Newest member of the Dream SMP",
    "Alternatives to toilet paper",
    "Alternatives to water",
    "Alternatives to excersize",
    "Alternatives to socalizing",
    "Alternatives to among us",
    "Alternatives to GE AC4400CW",
    "POV you get politicol views off TikTok",
    "POV you get politicol views off Twitter",
    "POV you get politicol views off Facebook",
    "POV you get politicol views off 4Chan",
    "POV you get politicol views off Discord",
    "But she said she was 18",
    "Fullproof way to get a million subscribers",
    "Fullproof way to make a million dollars",
    "Ways to get rich",
    "Reasons to move to Canada",
    "Reasons to move to Japan",
    "Reasons to sell Montana",
    "Cursed Roblox",
    "Reasons for after-birth abortion",
    "Instant turnoffs",
    "Instant turnons",
    "Things that should be legal",
    "Things that should be illegal",
    "Should be an album cover",
    "Apples new logo",
    "Microsofts new logo",
    "Playboys new logo",
    "Teslas new logo",
    "Best investment",
    "Worst investment",
    "Honesty & integrity",
    "How to cheat on a test",
    "How to cheat on your spouse",
    "Why did she take the kids",
    "Best fandom",
    "People with autism",
    "Elon Musks next company",
    "#1 New York Times Best Seller",
    "Things with exponential growth",
    "People named Deborah",
    "Sussiest things",
    "Worst type of Cancer",
    "Help! My nipple fell off!"
]

#################
# Extra Methods #
#################

# @delay
# Decorator applied to a method
# that causes a delay before
# execution of param delay
def delay(delay=0.):
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap

# killGame
# Wrapped with delay of 30 seconds
# so it deletes a game session and 
# the images in its folder 30 seconds 
# after being called
@delay(30.0)
def killGame(code):
    if code in games.keys():
        del games[code]
        if os.path.isdir(f'static/uploads/{code}'):
            #os.remove(f'static/uploads/{code}')
            for fn in os.listdir(f'static/uploads/{code}'):
                os.remove(f'static/uploads/{code}/{fn}')
            os.rmdir(f'static/uploads/{code}')

        else:
            pass # something may have gone pretty wrong, 
                 # or just nobody ever submitted images

        # manually clear dir: $ rm -r *


# formatImg
# Formats base64 image and saves to database
# Returns URL of image to display
def formatImg(code, img):
    if img != 'NOIMAGE':
        src = img.split(',')
        data = src[1]
        ext = ((src[0].split('/'))[1].split(';'))[0]
        if not os.path.isdir(f'static/uploads'):
            os.mkdir(f'static/uploads')
        if not os.path.isdir(f'static/uploads/{code}'):
            os.mkdir(f'static/uploads/{code}')
        name = str(time.time()).split('.')
        filename = f'uploads/{code}/{name[0]}{name[1]}.{ext}'
        with open('static/' + filename, 'wb') as f:
            f.write(base64.decodebytes(data.encode("ascii")))
        return url_for("static", filename=filename)
    else:
        return url_for("static", filename='img/noimg.png')

# randomPrompt
# Return a random prompt from the list of prompts
def randomPrompt():
    return prompts[random.randint(0,len(prompts))-1]

#######################
# Applictation Routes #
#######################

# index - /
# The main page
# Creates a game if returns post for
# creating a game
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        loop = True
        while (loop):
            code = random.randint(1000,9999)
            loop = code in games.keys()     
        games[str(code)] =  {
            'time': int(time.time()),
            'players': [],
            'host': 'NoHost',
            'round': 1,
            'prompts': [],
            'history': {},
            'subs': {},
            'endtime': 'NOTSET',
            'votes': {},
            'tvotes': {}
        }
        return redirect(f"/host/{code}")
    return render_template('index.html')

# searchCode - /join
# Takes post for code and finds the game 
# for that code, if found connects
@app.route('/join/', methods=['GET', 'POST'])
def searchCode():
    errormsg = ""
    if request.method == 'POST':
        code = int(request.form['code'])
        if str(code) in games.keys():
            return redirect(f"/join/{code}")
        else:
            errormsg = "That game dosen't exist!"
    return render_template('join.html', errormsg=errormsg)

# hostGame - /host/{code}
# Handles host joining with name through post
@app.route('/host/<code>', methods=['GET', 'POST'])
def hostGame(code):
    errormsg = ""
    if code in games.keys():
        if games[code]['host'] == 'NoHost':
            if request.method == 'POST':
                name = request.form['name']
                if name not in games[code]['players']:
                    session['name'] = name
                    session['game'] = code
                    games[code]['players'].append(name)
                    games[code]['host'] = name
                    return redirect(f'/play/{code}')
                else:
                    errormsg = "Name not available!"
            return render_template('name.html', gcode=code, errormsg=errormsg)
        else:
            return redirect(f'/join/{code}')
    else:
        #return render_template('error.html', error="This code does not exist!")
        return redirect('/')

# joinGame - /join/{code}
# Handles player joining with name through post
@app.route('/join/<code>', methods=['GET', 'POST'])
def joinGame(code):
    errormsg = ""
    if code in games.keys():
        if request.method == 'POST':
            if len(games[code]['players']) < players:
                name = request.form['name']
                if name not in games[code]['players']:
                    session['name'] = name
                    session['game'] = code
                    games[code]['players'].append(name)
                    return redirect(f'/play/{code}')
                else:
                    errormsg = "Name not available!"
            else:
                errormsg = "Game is full!"
        return render_template('name.html', gcode=code, errormsg=errormsg)
    else:
        #return render_template('error.html', error="This code does not exist!")
        return redirect('/join')

# gameLobby - /play/{code}
# Handles the lobby page before the game starts
# Can be started by host button
@app.route('/play/<code>')
def gameLobby(code):
    if code in games.keys():
        if code == session['game']:
            if session['name'] in games[code]['players']:
                emit('serverUpdatePlayers', 
                     games[code]['players'], 
                     to=code, 
                     namespace=f'/play/{code}'
                     )
                return render_template('lobby.html',
                                       hostn=games[code]['host'], 
                                       gcode=code, 
                                       players=games[code]['players'], 
                                       name=session['name']
                                       )
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

# playGame - /play/{code}/game
# Handles the rounds for the game
@app.route('/play/<code>/game')
def playGame(code):
    if code in games.keys():
        if code == session['game']:
            if session['name'] in games[code]['players']:
                if games[code]['round'] <= rounds*2:
                    if games[code]['round'] % 2 == 1:
                        games[code]['votes'] = {}
                        return render_template('game.html', 
                                                hostn=games[code]['host'], 
                                                _round=games[code]['round'], 
                                                gcode=code, 
                                                players=games[code]['players'], 
                                                name=session['name']
                                                )
                    else:
                        return render_template('vote.html', 
                                                hostn=games[code]['host'], 
                                                _round=games[code]['round'], 
                                                gcode=code, 
                                                players=games[code]['players'], 
                                                name=session['name']
                                                )
                else:
                    scores = {}
                    for player in games[code]['tvotes'].keys():
                        scores[player] = 0
                        for n in games[code]['tvotes'][player].keys():
                            scores[player] += games[code]['tvotes'][player][n]
                    #return f"<h2>Game Over</h2><code><pre>{scores}</pre></code>"
                    scores = dict(sorted(scores.items(), key=lambda item: item[1]))
                    killGame(code)
                    return render_template('scores.html', 
                                           gcode=code, 
                                           scores=scores, 
                                           name=session['name']
                                           )
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

#################
# Socket Events #
#################

# -> newPlayerJoin 
# A new player has joined to the lobby
# Emits the data for the new player in
# serverUpdatePlayers -> 
@socketio.event
def newPlayerJoin(block):
    name = str(block['name'])
    code = str(block['code'])
    if code in games.keys():
        if name in games[code]['players']:
            if name == session['name']:
                join_room(code)
                emit('serverUpdatePlayers', 
                     games[code]['players'], 
                     to=code
                     ) #, namespace=f'/play/{code}')
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

# -> startGame 
# The game has been requested to start
# Validates host, moves on server,
# and tells clients to move using emit
# serverStartGame ->
# On error emits error through
# serverCantStartGame ->
@socketio.event
def startGame(block):
    name = str(block['name'])
    code = str(block['code'])
    host = str(block['host'])
    if code in games.keys():
        if host == name:
            if host == games[code]['host']:
                if players > len(games[code]['players']) > 1:
                    emit('serverStartGame', '', to=code) 
                    #, namespace=f'/play/{code}')
                else:
                    emit('serverCantStartGame', 
                         'Insufficient player count!', 
                         to=code
                         ) #, namespace=f'/play/{code}')
            else:
                emit('serverCantStartGame', 
                     'Host not validated!', 
                     to=code
                     ) #, namespace=f'/play/{code}')
        else:
            emit('serverCantStartGame', 
                 'Host not validated!', 
                 to=code
                 ) #, namespace=f'/play/{code}')
    else:
        emit('serverCantStartGame', 
             'This game does not exist! (this is a bad server error)', 
             to=code
             ) #, namespace=f'/play/{code}')

# -> needPrompt 
# Returns the randomly generated prompt 
# through emit
# promptLoad ->
@socketio.event 
def needPrompt(block):
    name = str(block['name'])
    code = str(block['code'])
    #host = str(block['host'])
    _round = str(block['round'])
    if code in games.keys():
        if name in games[code]['players']:
            if int(_round) == games[code]['round']:
                if games[code]['round'] % 2 == 1:
                    join_room(code)
                    if _round not in games[code]['history'].keys():
                        needPrompt = True
                        while (needPrompt):
                            prompt = randomPrompt()
                            needPrompt = prompt in games[code]['prompts']
                        games[code]['history'][_round] = prompt
                    else:
                        prompt = games[code]['history'][_round]
                    emit('promptLoad', prompt, to=code)
                else:
                    if str(int(_round)-1) in games[code]['history'].keys():
                        join_room(code)
                        prompt = games[code]['history'][str(int(_round)-1)]
                        emit('promptLoad', prompt, to=code)
                    else:
                        pass
            else:
                pass
        else:
            pass
    else:
        pass

# -> needSubbedPlayers 
# Client is asking for the players
# that have submitted, names are 
# sent through emit
# playerSubbed ->
@socketio.event
def needSubbedPlayers(block):
    name = str(block['name'])
    code = str(block['code'])
    #host = str(block['host'])
    _round = str(block['round'])
    if code in games.keys():
        if name in games[code]['players']:
            if int(_round) == games[code]['round']:
                if games[code]['round'] % 2 == 1:
                    join_room(code)
                    if _round in games[code]['subs'].keys():
                        emit('playerSubbed', 
                             games[code]['subs'][_round], 
                             to=code
                             )
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

# -> imgSubmit 
# Client submits and image which
# the server processes and then
# sends confirmation through emit
# playerSubbed ->
# and notification that all players 
# have submitted through emit
# allPlayersSubbed ->
@socketio.event 
def imgSubmit(block):
    name = str(block['name'])
    code = str(block['code'])
    #host = str(block['host'])
    _round = str(block['round'])
    src = str(block['src'])
    if code in games.keys():
        if name in games[code]['players']:
            if int(_round) == games[code]['round']:
                if games[code]['round'] % 2 == 1:
                    join_room(code)
                    fn = formatImg(code, src)
                    if _round not in games[code]['subs'].keys():
                        games[code]['subs'][_round] = {}
                    games[code]['subs'][_round][name] = fn
                    subbedKeys = sorted(list(games[code]['subs'][_round].keys()))
                    if subbedKeys == sorted(games[code]['players']):
                        emit('allPlayersSubbed', '', to=code)
                        games[code]['endtime'] = 'NOTSET'
                        games[code]['round'] += 1
                    emit('playerSubbed', games[code]['subs'][_round], to=code)
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

# -> adminOverideSum 
# Host client requests to skip
# section; validates host and 
# returns a notification of it
# through emit 
# allPlayersSubbed ->
@socketio.event
def adminOverideSub(block):
    name = str(block['name'])
    code = str(block['code'])
    host = str(block['host'])
    _round = str(block['round'])
    if code in games.keys():
        if host == name:
            if host == games[code]['host']:
                if int(_round) == games[code]['round']:
                    if _round not in games[code]['subs'].keys():
                        games[code]['subs'][_round] = {}   
                    for player in games[code]['players']:
                        if player not in games[code]['subs'][_round].keys():
                            fn = url_for('static', filename='img/noimg.png')
                            games[code]['subs'][_round][player] = fn        
                    emit('allPlayersSubbed', '', to=code)
                    games[code]['endtime'] = 'NOTSET'
                    games[code]['round'] += 1 
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

# -> getImagesForVote 
# Client requests images so it
# can vote on them, this is
# filled through emit 
# imagesForVote ->
@socketio.event
def getImagesForVote(block):
    name = str(block['name'])
    code = str(block['code'])
    #host = str(block['host'])
    _round = str(block['round'])
    if code in games.keys():
        if name in games[code]['players']:
            if int(_round) == games[code]['round']:
                if games[code]['round'] % 2 == 0:
                    join_room(code)
                    if str(int(_round)-1) in games[code]['subs'].keys():
                        emit('imagesForVote', 
                             games[code]['subs'][str(int(_round)-1)], 
                             to=code
                             )
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

# -> getTimer 
# Client requests the endtime 
# and state for the end of the 
# voting and viewing section of
# the round; request filled
# through emit 
# timerUpdate ->
@socketio.event 
def getTimer(block):
    name = str(block['name'])
    code = str(block['code'])
    host = str(block['host'])
    _round = str(block['round'])
    if code in games.keys():
        if name in games[code]['players']:
            if int(_round) == games[code]['round']:
                join_room(code)
                if host == games[code]['host']:
                    if games[code]['endtime'] == 'NOTSET':
                        t = int(time.time())
                        games[code]['endtime'] = t+40
                    state = 'A'
                    if time.time() >= games[code]['endtime']:
                        games[code]['round'] += 1
                        state = 'C'
                    elif time.time() + 10 >= games[code]['endtime']:
                        state = 'B'
                    resp = {
                        'endtime': str(games[code]['endtime']), 
                        'state': state
                        }
                emit('timerUpdate', resp, to=code)
                '''me being stupid
                if int(time.time()) >= games[code]['endtime'] -1:
                    games[code]['round'] = 100
                    #eit('gameOver', '', to=code) 
                '''
            else:
                pass
        else:
            pass
    else:
        pass

# -> sendVote 
# Client lets the server
# know that it has casted a vote
# so it can be filled along 
# with the users identity
@socketio.event 
def sendVote(block):
    name = str(block['name'])
    code = str(block['code'])
    #host = str(block['host'])
    _round = str(block['round'])
    vote = str(block['vote'])
    if code in games.keys():
        if name in games[code]['players']:
            if int(_round) == games[code]['round']:
                join_room(code)
                games[code]['votes'][name] = vote
            else:
                pass
        else:
            pass
    else:
        pass

# -> getVotes 
# Client requests the number of votes
# so they can be displayed
# Thse are sent through emit
# displayVotes ->
@socketio.event 
def getVotes(block):
    name = str(block['name'])
    code = str(block['code'])
    #host = str(block['host'])
    _round = str(block['round'])
    if code in games.keys():
        if name in games[code]['players']:
            if int(_round) == games[code]['round']:
                join_room(code)
                votes = {}
                for player in games[code]['players']:
                    votes[player] = 0
                for voter in games[code]['votes'].keys():
                    votes[games[code]['votes'][voter]] += 1
                for player in votes.keys():   
                    if player not in games[code]['tvotes'].keys():
                        games[code]['tvotes'][player] = {}
                    games[code]['tvotes'][player][_round] = votes[player]  
                    #games[code]['tvotes'].update({player: nt})
                emit('displayVotes', votes, to=code)
            else:
                pass
        else:
            pass
    else:
        pass

#################
# Error Handles #
#################

# 404 - not found
# returns a redirect to main page
@app.errorhandler(404)
def Not_Found(e):
    return redirect('/')


####################
# Main Entry Point #
####################

# __main__ entry point
# Starts the application
if __name__ == '__main__':
    #socketio.run(app)
    socketio.run(app, debug=True)

#_#
