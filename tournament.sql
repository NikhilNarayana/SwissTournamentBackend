-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
'CREATE TABLE players (id integer NOT NULL, 
	name text NOT NULL, 
	PRIMARY KEY (id)
	);'
'CREATE TABLE matches (m_id integer NOT NULL, 
	player1 integer, 
	player2 integer, 
	PRIMARY KEY (m_id), 
	FOREIGN KEY (player1) REFERENCES players(id), 
	FOREIGN KEY (player2) REFERENCES players(id)
	);'
'CREATE TABLE standings (
    p_id integer NOT NULL,
    win integer DEFAULT 0,
    lose integer DEFAULT 0,
    tie integer DEFAULT 0,
    FOREIGN KEY (p_id) REFERENCES players(id)
);'
'CREATE VIEW summatches AS SELECT standings.p_id,
    ((COALESCE(standings.win, 0) + COALESCE(standings.lose, 0)) + COALESCE(standings.tie, 0)) AS sum FROM standings;'
