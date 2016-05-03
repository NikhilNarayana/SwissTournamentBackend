# SwissTournamentBackend

This is a backend for a Swiss bracket tournament. It employs PostgreSQL and Python to quickly get data necessary for the front end.

## SET UP
Setting up the project is simple:

1. Navigate to the project directory in terminal.
2. Open up psql
3. Type in `\i tournament.sql`

That will create the tournament SQL database and now you can run the tournament_test.py to check that the code is working properly.

## PSQL Structure
### Players
| Column        | Type           |Modifiers  |
| ------------- |:-------------:| -----:|
| id      | integer (serial) | not null default nextval('players_id_seq'::regclass) |
| name | text | not null |

### Matches
| Column | Type | Modifiers |
| ------ |:--------:|-------:|
|m_id | integer (serial) | not null default nextval('players_id_seq'::regclass) |
|player1 | integer | |
|player2 | integer | |

+ Indexes: "matches_pkey" PRIMARY KEY, btree (m_id)
+ Foreign-key constraints: "matches_player1_fkey" FOREIGN KEY (player1) REFERENCES players(id) AND "matches_player2_fkey" FOREIGN KEY (player2) REFERENCES players(id)
    
### Standings
| Column        | Type           | Modifiers  |
| ------------- |:-------------:| -----:|
| p_id | integer | not null |
| win  | integer | default 0 |
| lose | integer | default 0 |
| tie  | integer | default 0 |

+ Foreign-key constraints: "records_p_id_fkey" FOREIGN KEY (p_id) REFERENCES players(id)

### SumMatches
| Column | Type | Modifiers |
| ------ |:----:|----------:|
| p_id | integer |          |
| sum  | integer |          |
