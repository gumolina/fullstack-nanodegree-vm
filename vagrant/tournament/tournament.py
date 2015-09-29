#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
"Import needed libraries"
import psycopg2
import contextlib

@contextlib.contextmanager
def get_cursor():
    """ Connect to database and set the cursor. 
    After the with get_cursor is finished, commit and close the connection """
    conn = connect()
    cur = conn.cursor()
    try:
        yield cur
    except:
        raise
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM matches;")

def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM players")

def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as cursor:
        cursor.execute("select count(*) from players")
        result = cursor.fetchone()
    return result[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as cursor:
        cursor.execute("INSERT INTO players(name) VALUES (%s);",[name])
    
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
    with get_cursor() as cursor:
        cursor.execute("select player_id, player_name, wins, wins+losses as matches from rank")
        result = cursor.fetchall()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with get_cursor() as cursor:
        cursor.execute("INSERT INTO matches(winner_id,loser_id) VALUES (%s,%s);",[winner,loser])
    
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

    "Fetch all players per rank (victories)"
    with get_cursor() as cursor:
        cursor.execute("select player_id, player_name from rank")
        rows = cursor.fetchall()
    
    "Create an empty list"    
    result = []

    "Repeat while the number of players fetched in the query is still >0"
    while rows:
        """Add auxiliary number (in the future, it would be easier to check whether the match already happened,
            if so, we can fetch the next player"""
        aux = 1
        """ Set 1st player of the match as the top on the rank (row 0)"""
        player1 = rows[0]
        """ Set the 2nd player of the match as the 2nd on the rank (row aux = 1)"""
        player2 = rows[aux]
        """ After players are set, we can delete those entries from the list"""
        del rows[aux]
        del rows[0]
        """ Finally, insert the match to the result list"""
        result.append(player1 + player2)
        
    """ Return the all the final matches"""   
    return result