import os
import csv
import argparse
import hashlib
import zipfile
import configparser
import datetime
import logging.config
import yaml
import json
import psycopg2
import getpass
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_db(db_password, hostname, username):
    try:
        connection = psycopg2.connect(user=username,
                                      password=db_password,
                                      host=hostname,
                                      port="5432",
                                      database="postgres")

        connection.autocommit = True
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()
        find_db_query = "SELECT datname FROM pg_catalog.pg_database WHERE datname = 'postgres'"
        cursor.execute(find_db_query)

        if cursor.fetchone():
            pass
        else:
            create_table_query = "CREATE DATABASE postgres;"

            cursor.execute(create_table_query)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)
    finally:

        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            logger.info("PostgreSQL connection is closed")


def create_table(db_password, hostname, username):
    connection = None
    try:
        connection = psycopg2.connect(user=username,
                                      password=db_password,
                                      host=hostname,
                                      port="5432",
                                      database="postgres")

        connection.autocommit = True
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()

        # create_db(db_password, hostname, username)

        cursor.execute("select * from information_schema.tables where table_name=%s", ('listdir',))
        print(bool(cursor.rowcount))
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
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)
    finally:

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            logger.info("PostgreSQL connection is closed")


def setup_logging(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration from a yaml file.

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=default_level)


def zip_output(filename):
    """Accepts a desired filename,
    then zips that file.
        Args:
            filename : the filename of the zip file to be created
    """
    zip_name = filename + ".zip"
    with zipfile.ZipFile(zip_name, 'w') as out_zip:
        out_zip.write(filename)
        logger.info("Created zip file :" + zip_name)


def get_hash(file_path, hash_type):
    """Accepts a desired file_path,
    then hashes that file depending on the hash_mode.
        Args:
            file_path : the file to be hashed.
            hash_type : the hash type.
    """
    with open(file_path, 'rb') as afile:
        buf = afile.read()

        if hash_type == "sha1":
            sha1_hasher = hashlib.sha1()
            sha1_hasher.update(buf)
            logger.info("File : {}, returned hash(sha1) : {}".format(file_path, sha1_hasher.hexdigest()))
            return sha1_hasher.hexdigest()
        elif hash_type == "md5":
            md5_hasher = hashlib.md5()
            md5_hasher.update(buf)
            logger.info("File : {}, returned hash(md5) : {}".format(file_path, md5_hasher.hexdigest()))
            return md5_hasher.hexdigest()


def add_datetime(file_name, time_format):
    """Accepts a desired file_name,
    then formats the filename to include the current date and time.
        Args:
            file_name : the file to be formatted.
            time_format : the format of date time to be used.
    """
    curr_date = datetime.datetime.now()
    str_date = curr_date.strftime(time_format)
    logger.info("Time the file is created : {}".format(str_date))
    return str_date + "_" + file_name


def find_files(desired_path):
    dict = []
    for root, directories, files in os.walk(desired_path):

        for file in files:
            file_path = "{}{}{}".format(root, os.sep, file)

            file_dict = {"parent_path": os.path.dirname(root), "filename": file,
                         "filesize": os.path.getsize(file_path), "md5": get_hash(file_path, "md5"),
                         "sha1": get_hash(file_path, "sha1")}
            dict.append(file_dict)
    return dict


def create_csv(desired_path, desired_filename):
    """
    :param desired_path: the desired path to be recursively saved
    :param desired_filename: the desired filename output
    """
    desired_filename = add_datetime(desired_filename + ".csv", '%Y%m%d_%H-%M-%S')
    with open(desired_filename, 'w+', newline='') as csvfile:
        fieldnames_csv = ['parent_path', 'filename', 'filesize', 'md5', 'sha1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_csv)
        writer.writeheader()

        for lines in find_files(desired_path):
            writer.writerow(lines)
    zip_output(desired_filename)


def create_insert(desired_path, db_password, hostname, username):
    """
    :param desired_path: the desired path to be recursively saved
    :param db_password: the password of the database
    :param hostname: the hostname needed for db configuration
    :param username: the username needed for db configuration
    """
    try:
        connection = psycopg2.connect(user=username,
                                      password=db_password,
                                      host=hostname,
                                      port="5432",
                                      database="postgres")

        connection.autocommit = True
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        create_db(db_password, hostname, username)
        create_table(db_password, hostname, username)

        cursor = connection.cursor()
        insert_query = "INSERT INTO listdir(ParentPath, FileName, Size, MD5, sha1)" \
                       " VALUES(%(parent_path)s,%(filename)s,%(filesize)s,%(md5)s,%(sha1)s)"
        cursor.executemany(insert_query, find_files(desired_path))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)
    # finally:
    #     # closing database connection.
    #     if (connection):
    #         cursor.close()
    #         connection.close()
    #         logger.info("PostgreSQL connection is closed")


def create_json(desired_path, desired_filename):
    """
    :param desired_path: the desired path to be recursively saved
    :param desired_filename: the desired filename output
    """
    desired_filename = add_datetime(desired_filename + ".txt", '%Y%m%d_%H-%M-%S')
    with open(desired_filename, 'w+') as jsonfile:
        json.dump(find_files(desired_path), jsonfile, indent=2)
    zip_output(desired_filename)


def main():
    config = configparser.ConfigParser()
    conf_dir = os.path.join(os.path.dirname(__file__), 'conf.ini')
    config.read(conf_dir)
    directory = config['args']['directory']
    filename = config['args']['filename']
    hostname = config['args']['hostname']
    username = config['args']['username']

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs='?', default=directory, help="the directory to be recursively checked")
    parser.add_argument("csv_name", nargs='?', default=filename, help="the desired file name")
    parser.add_argument("-j", "--json", action="store_true", help="option to make the output a json")
    parser.add_argument("-c", "--csv", action="store_true", help="option to make the output a csv")
    parser.add_argument("-q", "--query", action=PwdAction, nargs=0, help="option to make the output"
                                                                         " save in the database")

    args = parser.parse_args()

    if os.path.exists(args.directory):
        try:
            if args.json:
                create_json(os.path.abspath(args.directory), args.csv_name)
            elif args.query:
                create_insert(os.path.abspath(args.directory), args.query, hostname, username)
            elif args.csv:
                create_csv(os.path.abspath(args.directory), args.csv_name)
        except Exception as e:
            logger.error('Error: ' + str(e), exc_info=True)
    else:
        print("Path not found")


class PwdAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        my_pass = getpass.getpass()
        setattr(namespace, self.dest, my_pass)


if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)
    main()
