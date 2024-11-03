import psycopg2
from decouple import config


def add_manager(manager_tg_id, name, last_name):
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO manager (tg_name, name, lastname) VALUES (%s, %s, %s)", (manager_tg_id, name, last_name))


def add_team(name_of_team, manager_tg_id, ):
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO team (name, manager) VALUES (%s, %s)", (name_of_team, str(manager_tg_id)))

# cursor.execute("INSERT INTO place (title, coordinates) VALUES (%s, %s)", ("3-я детская", ["42.875129495258, 74.58871443649852", "42.8750076264082, 74.58870169609429", "42.87507005769137, 74.58970093192504", "42.87495162861068, 74.58968617967531"]))

def add_employee(manager_tg_id, tg_id, name, lastname, ):
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM team WHERE manager = %s", (str(manager_tg_id), ))
            team = cursor.fetchone()
            cursor.execute("INSERT INTO employee (tg_name, name, lastname, team) VALUES (%s, %s, %s, %s)", (tg_id, name, lastname, team))
        

def add_place(title, coordinates, ):
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO place (title, coordinates) VALUES (%s, %s)", (title, coordinates))


def get_managers():
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM manager")
            return cursor.fetchall()


def get_manager(manager_tg_id):
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM manager WHERE tg_name=%s", (str(manager_tg_id), ))
            return cursor.fetchone()


def get_manager_by_employee(tg_id):
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT team FROM employee WHERE tg_name=%s", (str(tg_id), ))
            team_id = cursor.fetchone()
            cursor.execute("SELECT manager FROM team WHERE id=%s", (team_id, ))
            return cursor.fetchone()


# def get_team(manager_tg_id):
#     with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
#         conn.autocommit = True
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT * FROM manager WHERE tg_name=%s", (str(manager_tg_id), ))
#             return cursor.fetchone()


def get_places():
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM place")
            return cursor.fetchall()


def get_employees(manager_tg_id):
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM team WHERE manager = %s", (str(manager_tg_id), ))
            team = cursor.fetchone()
            cursor.execute("SELECT * FROM employee WHERE team=%s", (team, ))
            return cursor.fetchall()


def get_employee(tg_id):
    with psycopg2.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD')) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT (name, lastname) FROM employee WHERE tg_name=%s", (str(tg_id), ))
            # print(cursor.fetchone())
            return cursor.fetchone()
