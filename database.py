INSERT_POLL_RETURN_ID = "INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER);"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER);"""


SELECT_ALL_POLLS = "SELECT * FROM polls;"
SELECT_POLL_WITH_OPTIONS = """SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls.id = %s;"""

INSERT_OPTION = "INSERT INTO options (option_text, poll_id) VALUES %s;"
INSERT_VOTE = "INSERT INTO votes (username, option_id) VALUES (%s, %s);"


def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)


def get_polls(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()


def get_latest_poll(connection):
    with connection:
        with connection.cursor() as cursor:
            pass


def get_poll_details(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_WITH_OPTIONS, (poll_id,))
            return cursor.fetchall()


def get_poll_and_vote_results(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_VOTE_DETAILS, (poll_id,))
            return cursor.fetchall()


def get_random_poll_vote(connection, option_id):
    with connection:
        with connection.cursor() as cursor:
            pass


def create_poll(connection, title, owner, options):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))
            
            poll_id = cursor.fetchone()[0]
            option_values = [(option_text, poll_id) for option_text in options]
            
            from psycopg2.extras import execute_values
            execute_values(cursor, INSERT_OPTION, option_values)


def add_poll_vote(connection, username, option_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))

SELECT_RANDOM_VOTE = "SELECT * FROM votes WHERE option_id = %s ORDER BY RANDOM() LIMIT 1;"
def get_random_poll_vote(connection, option_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RANDOM_VOTE, (option_id,))
            return cursor.fetchone()
        

SELECT_LATEST_POLL_WITH_OPTIONS = """SELECT * FROM polls
 JOIN options ON polls.id = options.poll_id
 WHERE polls.id = (
     SELECT id FROM polls ORDER BY id DESC LIMIT 1
 );"""
SELECT_POLL_VOTE_DETAILS = """
SELECT
    options.id,
    options.option_text,
    COUNT(votes.option_id) as vote_count,
    COUNT(votes.option_id) * 100.0 / sum(count(votes.option_id)) as vote_percentage
FROM options
LEFT JOIN votes on options.id = votes.option_id
WHERE options.poll_id = %s
GROUP BY options.id;"""
SELECT_RANDOM_VOTE = "SELECT * FROM votes WHERE option_id = %s ORDER BY RANDOM() LIMIT 1;"