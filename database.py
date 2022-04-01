import sqlite3


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_blacklist_table(conn, table_name: str):
    """create a table with table name"""
    try:
        c = conn.cursor()
        c.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} (word TEXT NOT NULL UNIQUE);"
        )
    except Exception as e:
        raise (e)


def create_links_table(conn, table_name: str):
    """crate a table to store gatherd links"""
    try:
        c = conn.cursor()
        c.execute(
            f"""CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY,
            channel_username TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE);"""
        )
    except Exception as e:
        raise e


def setup_data(conn, blacklist_file: str, table_name: str):
    """setup db with predefind words in black list file"""
    black_list = [
        line.rstrip() for line in open(f"{blacklist_file}", "r", encoding="UTF-8")
    ]
    c = conn.cursor()
    counter = 0

    for word in black_list:
        counter += 1
        c.execute(f"""INSERT OR IGNORE INTO {table_name} (word) VALUES(?);""", (word,))
        if counter % 10 == 0:
            conn.commit()
    conn.commit()


def is_present(conn, table_name: str, word: str) -> bool:
    """check presense of a word in a table"""
    c = conn.cursor()
    c.execute(f"""SELECT EXISTS(SELECT 1 FROM {table_name} WHERE word=?);""", (word,))
    answer = c.fetchone()[0]
    if answer == 0:
        return False
    elif answer == 1:
        return True
    else:
        raise Exception


def add_to_blacklist_db(conn, table_name: str, word: str):
    """add a word to black list"""
    c = conn.cursor()
    c.execute(f"""INSERT OR IGNORE INTO {table_name} (word) VALUES(?)""", (word,))
    conn.commit()


def remove_from_blacklist_db(conn, table_name: str, word: str):
    c = conn.cursor()
    c.execute(f"""DELETE FROM {table_name} WHERE word LIKE ?""", (word,))
    conn.commit()


def show_all_words_db(conn, table_name) -> str:
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    words = [word[0] for word in c.fetchall()]
    words = "\n".join(words) + "\n."
    return words


def show_all_links_db(conn, table_name) -> str:
    c = conn.cursor()
    c.execute(f"SELECT link FROM {table_name}")
    words = [word[0] for word in c.fetchall()]
    words = "\n".join(words)
    return words


def show_all_links_db_api(conn, table_name):
    c = conn.cursor()
    c.execute(f"SELECT link FROM {table_name}")
    words = [word[0] for word in c.fetchall()]
    return words


def add_to_links_db(conn, table_name, channel_username, link, post_date) -> None:
    c = conn.cursor()
    c.execute(
        f"""INSERT OR IGNORE INTO {table_name} (channel_username,link) VALUES(?,?)""",
        (channel_username, link),
    )
    conn.commit()
