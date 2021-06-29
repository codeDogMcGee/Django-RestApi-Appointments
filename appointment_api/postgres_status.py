from time import sleep
import psycopg2

def check_status(db_name, username, password, host, port):
    connected = False
    while connected is False:
        try:
            conn = psycopg2.connect(f'dbname={db_name} user={username} password={password} host={host} port={port}')
            if conn:
                print('Postgres is connected.')
                connected = True
                sleep(1)
        except Exception as e:
            print(e)
            print('Try again in 1 second.')
            sleep(1)
