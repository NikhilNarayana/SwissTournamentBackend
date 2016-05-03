-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\connect tournament;
CREATE TABLE players (id serial NOT NULL, 
	name text NOT NULL, 
	PRIMARY KEY (id)
	);
CREATE TABLE matches (m_id serial NOT NULL, 
	player1 integer, 
	player2 integer,
	winner integer, 
	PRIMARY KEY (m_id), 
	FOREIGN KEY (player1) REFERENCES players(id), 
	FOREIGN KEY (player2) REFERENCES players(id)
	);
CREATE VIEW wins AS SELECT players.id, players.name, COUNT(matches.winner) AS wins FROM players LEFT JOIN matches ON players.id = matches.winner GROUP BY players.id;
CREATE VIEW match_counter AS SELECT players.id, players.name, COUNT(matches) AS matches_played FROM players LEFT JOIN matches ON players.id = matches.player1 OR players.id = matches.player2 GROUP BY players.id;
CREATE VIEW standings AS SELECT wins.id, wins.name, wins.wins, match_counter.matches_played FROM wins JOIN match_counter ON wins.id = match_counter.id ORDER BY wins DESC;