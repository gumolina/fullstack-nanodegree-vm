-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop tournament base to start from scratch
DROP database tournament;
-- Create tournament database and log in into it
create database tournament;
\c tournament

-- Create table players with ID and name
CREATE TABLE players (
   ID  SERIAL PRIMARY KEY,
   name VARCHAR(100) NOT NULL
   );

-- Create matches table with id, the winner and loser player ids. Also add Foreign Key
CREATE TABLE matches (
   ID  SERIAL PRIMARY KEY,
   winner_id int references players(id),
   loser_id int references players(id)
   );

-- Create view for ranking the players based on winnings. The view will have 4 columns:
-- player_id, player_name, number of winnings and number of losses
-- The views is then ordered in a way that the player with most winnings will be on top
CREATE VIEW rank AS 
	SELECT  p.id as player_id, p.name player_name, count(w.id) as wins, count(l.id) as losses 
				from players p 
            left join matches w on w.winner_id = p.id
            left join matches l on l.loser_id = p.id
            group by p.id
            order by wins desc;