#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# Finished in 
#

import psycopg2
import bleach
import re
import random
""" This application uses the psycopg2 DB-API and PostgreSQL. The PSQL database contains 3 tables and 1 view. The tables are
players (id, name), standings (p_id, wim, lose, tie), and matches (m_id, player1, player2). The view is summatches and takes the values from
standings (win, lose, tie) to get the total matches played per player.
"""

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM matches;")
    cursor.execute("UPDATE standings SET win = 0, lose = 0, tie = 0;") #reset 
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM standings;")
    cursor.execute("DELETE FROM players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT count(*) as num from players;")
    players = cursor.fetchall()
    DB.close()
    return int(players[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (bleach.clean(name),))
    cursor.execute("INSERT INTO standings (p_id) SELECT players.id from players WHERE players.name = %s;", (bleach.clean(name),))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("""SELECT players.id, players.name, standings.win, summatches.sum FROM players, standings, summatches 
    	WHERE players.id = standings.p_id AND summatches.p_id = players.id ORDER BY standings.win, players.id;""")
    standings = cursor.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT standings.win FROM standings WHERE standings.p_id = %s;" % bleach.clean(winner))
    winner_score = cursor.fetchone()
    addwin = winner_score[0]
    addwin += 1
    cursor.execute("SELECT standings.lose FROM standings WHERE standings.p_id = %s;" % bleach.clean(loser))
    loser_score = cursor.fetchone()
    addlose = loser_score[0] 
    addlose += 1
    cursor.execute("UPDATE standings SET win = %s WHERE p_id = %s;" % (addwin, bleach.clean(winner)))
    cursor.execute("UPDATE standings SET lose = %s WHERE p_id = %s;" % (addlose, bleach.clean(loser)))
    DB.commit()
    DB.close()

def get_first_id_pairings(match_pairings, cursor, DB):
	player1 = 0 # Location of player 1 id
	player2 = 1 # player 2 id location
	listofplayers = [] # generic list of players
	cursor.execute("SELECT players.id from players, standings WHERE players.id = standings.p_id ORDER BY standings.win, players.id") # get all player ids in order by wins and then id values
	players = cursor.fetchall() # put all those values into a variable
	for tup in players: # cycle through the players list for tuples and then for the player ids. Append each player id into the list
		for p_id in tup:
			listofplayers.append(p_id)
	random.shuffle(listofplayers) # Unlike the next function, this one is for the first turn only and forces randomization to make the matches fair
	while len(listofplayers) > player2:
		cursor.execute("INSERT INTO matches (player1, player2) VALUES (%s, %s)" % (listofplayers[player1], listofplayers[player2])) #insert the match record
		DB.commit()
		cursor.execute("SELECT name from players where id = %s or id = %s" % (listofplayers[player1], listofplayers[player2])) # get the names of the players
		names = cursor.fetchall()
		pair = []
		pair.append(listofplayers[player1]) #make the pair tuple
		pair.append(names[0][0])
		pair.append(listofplayers[player2])
		pair.append(names[1][0])
		match_pairings.append(pair) #add the pair tuple to match_pairings
		player1 += 2 # increment past player 2
		player2 += 2 # increment past player 1
        return match_pairings #kept getting an indentaion error when one indent block was deleted

def get_id_pairings(match_pairings, cursor, DB):
	"""Essentially the same function as the previous one, but takes out the randomization allowing the players of similar standings to play each other"""
	listofplayers = []
	player1 = 0
	player2 = 1
	cursor.execute("SELECT players.id from players, standings WHERE players.id = standings.p_id ORDER BY standings.win, players.id")
	players = cursor.fetchall()
	for tup in players:
    		for p_id in tup:
				listofplayers.append(p_id)
	while len(listofplayers) > player2:
		cursor.execute("INSERT INTO matches (player1, player2) VALUES (%s, %s)" % (listofplayers[player1], listofplayers[player2]))
		DB.commit()
		cursor.execute("SELECT name from players where id = %s or id = %s" % (listofplayers[player1], listofplayers[player2]))
		names = cursor.fetchall()
		pair = []
		pair.append(listofplayers[player1])
		pair.append(names[0][0])
		pair.append(listofplayers[player2])
		pair.append(names[1][0])
		match_pairings.append(pair)
		player1 += 2
		player2 += 2
    return match_pairings


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    match_pairings = []
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT sum FROM summatches;")
    tuple_round = cursor.fetchone()
    current_round = tuple_round[0] # Check the sum to find the current round. Sum = round because you play one match per round
    if current_round == 0:
    	match_pairings = get_first_id_pairings(match_pairings, cursor, DB)
    else:
    	match_pairings = get_id_pairings(match_pairings, cursor, DB)
    DB.close()
    return match_pairings
