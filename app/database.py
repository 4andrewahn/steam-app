"""Defines all the functions related to the database"""
from app import db

def fetch_games(searchword="") -> dict:
    """Reads all games listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select queryID, name, releaseDate, headerImage, detailedDescript from SteamGames WHERE name LIKE '%%{}%%' limit 80;".format(searchword)).fetchall()
    conn.close()
    games_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
            "releaseDate": result[2],
            "headerImage": result[3],
            "detailedDescript": result[4]
        }
        games_list.append(item)

    return games_list


def update_task_entry(task_id: int, text: str) -> None:
    """Updates game description based on given `game_id`

    Args:
        game_id (int): Targeted game_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update SteamGames set name = "{}" where queryID = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_title_entry(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update SteamGames set name = "{}" where queryID = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()

"""
Insert new game to database.
Returns: The queryID for the inserted entry
"""
def insert_new_game(text: str) ->  int:
    conn = db.connect()
    id_query = conn.execute("Select queryID FROM SteamGames;").fetchall()
    last_id = max(id_query, key=lambda x: x[0])[0]
    insert_id = last_id + 1
    query = 'Insert Into SteamGames (queryID, name) VALUES ("{}", "{}");'.format(
        insert_id, text)
    try:
        conn.execute(query)
    except Exception as e:
        print("Error message: " + str(e))
        return -1
    
    conn.close()

    return insert_id


""" remove entries based on game ID """
def remove_game_by_id(game_id: int) -> None:
    conn = db.connect()
    query = 'Delete From SteamGames where queryID={};'.format(game_id)
    conn.execute(query)
    conn.close()

def run_advanced_query() -> dict:
    conn = db.connect()
    query_results = conn.execute("""SELECT SteamGames.name, GenreIsCasual as Casual, GenreIsStrategy as Strategy, releaseDate
                                FROM SteamGames
                                JOIN Categories ON SteamGames.queryID = Categories.queryID
                                WHERE Categories.GenreIsCasual = 'TRUE' AND releaseDate like '%%soon%%'
                                UNION
                                SELECT SteamGames.name, GenreIsCasual as Casual, GenreIsStrategy as Strategy, releaseDate
                                FROM SteamGames
                                JOIN Categories ON SteamGames.queryID = Categories.queryID
                                WHERE Categories.GenreIsStrategy = 'TRUE' AND releaseDate like '%%soon%%' ORDER BY name ASC
                                LIMIT 15;""").fetchall()
    conn.close()
    games_list = []
    for result in query_results:
        item = {
            "name": result[0],
            "casual": result[1],
            "strategy": result[2],
            "releaseDate": result[3]
        }
        games_list.append(item)

    return games_list

def run_advanced_query_2() -> dict:
    conn = db.connect()
    query_results = conn.execute("""SELECT name, priceFinal, CategoryMultiplayer as Multiplayer FROM SteamGames NATURAL JOIN Categories
                                    WHERE queryID IN (
                                        SELECT queryID
                                        FROM GameCommunity
                                        WHERE recommendations > 49999
                                    )
                                    ORDER BY PriceFinal ASC LIMIT 15;""").fetchall()
    conn.close()
    games_list = []
    for result in query_results:
        item = {
            "name": result[0],
            "priceFinal": result[1],
            "multiplayer": result[2]
        }
        games_list.append(item)

    return games_list


def check_for_procedure(num):
    conn = db.connect()
    res = conn.execute(f"SHOW PROCEDURE STATUS WHERE Name = 'procedure{num}';")
    conn.close()
    if res.fetchone() is None:
        return False
    return True

def create_stored_procedure1() -> None:
    conn = db.connect()
    conn.execute("""
        CREATE PROCEDURE procedure1()
        BEGIN
            DECLARE vName VARCHAR(50);
            DECLARE vPopularity VARCHAR(12);
            DECLARE vRecs INT;

            DECLARE exit_loop BOOLEAN DEFAULT FALSE;

            DECLARE gamesCursor CURSOR FOR (
                SELECT name, recommendations
                FROM SteamGames NATURAL JOIN GameCommunity
                WHERE recommendations > 1000 AND queryID IN (
                    SELECT queryID
                    FROM Categories
                    WHERE CategoryMultiplayer = 'TRUE'
                )
                ORDER BY recommendations 
            );

            DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;

            DROP TABLE IF EXISTS NewTable; 

            CREATE TABLE NewTable (
                Name VARCHAR(50) PRIMARY KEY,
                Popularity VARCHAR(12),
                Recs INT
            );

            OPEN gamesCursor; 
                cloop: LOOP
                FETCH gamesCursor INTO vName, vRecs; 

                IF exit_loop THEN
                    LEAVE cloop;
                END IF; 

                IF vRecs > 50000 THEN
                    SET vPopularity = "Popular";
                ELSEIF vRecs > 25000 THEN
                    SET vPopularity = "Well-Liked";
                ELSEIF vRecs > 10000 THEN
                    SET vPopularity = "Liked";
                ELSE
                    SET vPopularity = "Average";
                END IF; 

                INSERT IGNORE INTO NewTable VALUE (vName, vPopularity, vRecs);
                END LOOP cloop; 
            CLOSE gamesCursor; 

            SELECT Name, Popularity
            FROM NewTable
            ORDER BY Recs DESC; 
        END;
    """)
    conn.close()

def run_stored_procedure1():
    conn = db.connect()
    query_results = conn.execute("CALL procedure1()")
    conn.close()
    items = []
    for entry in query_results:
        item = {
            "name": entry[0],
            "popularity": entry[1]
        }
        items.append(item)
    return items

def create_stored_procedure2() -> None:
    conn = db.connect()
    conn.execute("""
        CREATE PROCEDURE procedure2()
        BEGIN
            DECLARE vName VARCHAR(50);
            DECLARE vPopularity VARCHAR(12);
            DECLARE vRecs INT;

            DECLARE exit_loop BOOLEAN DEFAULT FALSE;

            DECLARE gamesCursor CURSOR FOR (
                SELECT name, recommendations
                FROM SteamGames NATURAL JOIN GameCommunity
                WHERE recommendations > 1000 AND queryID IN (
                    SELECT queryID
                    FROM Categories
                    WHERE CategorySinglePlayer = 'TRUE'
                )
                ORDER BY recommendations 
            );

            DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;

            DROP TABLE IF EXISTS NewTable; 

            CREATE TABLE NewTable (
                Name VARCHAR(50) PRIMARY KEY,
                Popularity VARCHAR(12),
                Recs INT
            );

            OPEN gamesCursor; 
                cloop: LOOP
                FETCH gamesCursor INTO vName, vRecs; 

                IF exit_loop THEN
                    LEAVE cloop;
                END IF; 

                IF vRecs > 50000 THEN
                    SET vPopularity = "Popular";
                ELSEIF vRecs > 25000 THEN
                    SET vPopularity = "Well-Liked";
                ELSEIF vRecs > 10000 THEN
                    SET vPopularity = "Liked";
                ELSE
                    SET vPopularity = "Average";
                END IF; 

                INSERT IGNORE INTO NewTable VALUE (vName, vPopularity, vRecs);
                END LOOP cloop; 
            CLOSE gamesCursor; 

            SELECT Name, Popularity
            FROM NewTable
            ORDER BY Recs DESC; 
        END;
    """)
    conn.close()

def run_stored_procedure2():
    conn = db.connect()
    query_results = conn.execute("CALL procedure2()")
    conn.close()
    items = []
    for entry in query_results:
        item = {
            "name": entry[0],
            "popularity": entry[1]
        }
        items.append(item)
    return items


def check_for_trigger():
    conn = db.connect()
    res = conn.execute(f"SHOW TRIGGERS WHERE `Trigger` = 'addGameTrigger';")
    conn.close()
    if res.fetchone() is None:
        return False
    return True


def create_trigger() -> None:
    conn = db.connect()
    conn.execute("""
        CREATE TRIGGER addGameTrigger
            BEFORE INSERT ON SteamGames
            FOR EACH ROW
        BEGIN
            IF EXISTS (SELECT 1 FROM SteamGames WHERE name = NEW.name) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'A game with the same name already exists';
            END IF;
        END;
    """)
    conn.close()