-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP database tournament;
create database tournament;
\c tournament

CREATE TABLE players (
   ID  SERIAL PRIMARY KEY,
   name VARCHAR(100) NOT NULL
   );

CREATE TABLE matches (
   ID  SERIAL PRIMARY KEY,
   winner_id int references players(id),
   loser_id int references players(id)
   );

CREATE VIEW rank AS 
	SELECT  p.id as player_id, p.name player_name, count(w.id) as wins, count(l.id) as losses 
				from players p 
            left join matches w on w.winner_id = p.id
            left join matches l on l.loser_id = p.id
            group by p.id
            order by wins desc;