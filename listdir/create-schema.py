import psycopg2
import argparse
import configparser
import os
import getpass


def create_db(db_password, hostname, username):
    try:
        connection = psycopg2.connect(user=username,
                                      password=db_password,
                                      host=hostname,
                                      port="5432",
                                      database="postgres")

        cursor = connection.cursor()
        find_db_query = "SELECT datname FROM pg_catalog.pg_database WHERE datname = 'listdirDB'"
        cursor.execute(find_db_query)

        if bool(cursor.rowcount):
            pass
        else:
            create_table_query = "CREATE DATABASE postgres;"

            cursor.execute(create_table_query)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:

        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def create_table(db_password, hostname, username):
    try:
        connection = psycopg2.connect(user=username,
                                      password=db_password,
                                      host=hostname,
                                      port="5432",
                                      database="postgres")

        cursor = connection.cursor()

        create_db(db_password, hostname, username)

        cursor.execute("select * from information_schema.tables where table_name=%s", ('listdir',))

        if bool(cursor.rowcount):
            pass
        else:
            create_table_query = "CREATE TABLE listdir(" \
                                 "ID SERIAL PRIMARY KEY NOT NULL," \
                                 "ParentPath VARCHAR," \
                                 "FileName VARCHAR," \
                                 "Size VARCHAR," \
                                 "MD5 VARCHAR," \
                                 "sha1 VARCHAR);"

            cursor.execute(create_table_query)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def main():
    config = configparser.ConfigParser()
    conf_dir = os.path.join(os.path.dirname(__file__), 'conf.ini')
    config.read(conf_dir)
    hostname = config['args']['hostname']
    username = config['args']['username']

    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", action=PwdAction, nargs=0)
    args = parser.parse_args()
    create_table(args.query, hostname, username)


class PwdAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        my_pass = getpass.getpass()
        setattr(namespace, self.dest, my_pass)


if __name__ == '__main__':
    main()