def get_connection():
    pass

def tables(conn):
    """
    Crea las tablas de la db.
    """
    
    sql_query = """
    CREATE TABLE IF NOT EXISTS app_user(
        user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT now()
    );
    
    CREATE TABLE IF NOT EXISTS player
    (
        puuid VARCHAR(78) PRIMARY KEY,
        player_name TEXT NOT NULL,
        player_level INTEGER NOT NULL CHECK (player_level >= 0),
        player_icon INTEGER,
        updated_at TIMESTAMPTZ DEFAULT now()
    );
    
    CREATE TABLE IF NOT EXISTS user_riot_link(
        app_user_id INTEGER NOT NULL REFERENCES app_user(user_id) ON DELETE CASCADE,
        player_puuid VARCHAR(78) NOT NULL REFERENCES player(puuid) ON DELETE CASCADE,
        PRIMARY KEY (app_user_id, player_puuid)
    );
    
    CREATE TABLE IF NOT EXISTS lol_match 
    (
        match_id VARCHAR(50) PRIMARY KEY,
        duration_seconds INTEGER NOT NULL CHECK (duration_seconds > 0),
        game_mode VARCHAR(25) NOT NULL,
        game_status VARCHAR(20) NOT NULL,
        patch_version VARCHAR(30)
    );
    
    CREATE TABLE IF NOT EXISTS champion
    (
        champion_id INTEGER PRIMARY KEY,
        champion_name VARCHAR(20) NOT NULL,
        champion_key VARCHAR(25)
    );
    
    CREATE TABLE IF NOT EXISTS match_participation
    (
        participation_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        match_id VARCHAR(50) NOT NULL REFERENCES lol_match(match_id) ON DELETE CASCADE,
        puuid VARCHAR(78) NOT NULL REFERENCES player(puuid) ON DELETE CASCADE,
        champion_id INTEGER NOT NULL REFERENCES champion(champion_id),
        kills INTEGER CHECK (kills >= 0),
        assists INTEGER CHECK (assists >= 0),
        deaths INTEGER CHECK (deaths >= 0),
        total_damage INTEGER CHECK (total_damage >= 0),
        damage_per_min NUMERIC(6,1),
        lane VARCHAR(20),
        champion_level INTEGER CHECK (champion_level >= 0),
        item_slots INT[],
        trinket INTEGER,
        total_minions INTEGER CHECK (total_minions >= 0),
        vision_score INTEGER CHECK (vision_score >= 0),
        kda NUMERIC(5,1),
        kp NUMERIC(3,2),
        win BOOLEAN NOT NULL,
        UNIQUE (match_id, puuid)
    );
    
    CREATE INDEX IF NOT EXISTS idx_mpart_puuid     ON match_participation (puuid);   
    CREATE INDEX IF NOT EXISTS idx_match_participation_champion ON match_participation (champion_id);
    """