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
        logger.info("Created zip file :"+zip_name)


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


def create_json(dict, desired_filename):
    os.remove(desired_filename)
    with open(desired_filename, 'w+') as jsonfile:
        json.dumps(dict, jsonfile, indent=2)
    zip_output(desired_filename)


def find_files(desired_path):
    dict = []
    for root, directories, files in os.walk(desired_path):

        for file in files:
            file_path = "{}{}{}".format(root, os.sep, file)

            file_dict = {"parent path": os.path.dirname(root), "filename": file,
                         "filesize": os.path.getsize(file_path), "md5": get_hash(file_path, "md5"),
                         "sha1": get_hash(file_path, "sha1")}
            dict.append(file_dict)
    return dict


def directory_to_csv(desired_path, desired_filename, is_json):
    """Accepts a desired path and a desired filename,
    then use the directory to recursively collect data then print in a csv file.
    Args:
        desired_path : the directory to be processed
        desired_filename : the filename of the csv to be created
        is_json : checks if the output will be json or a csv
    """
    if os.path.exists(desired_path):
        if is_json:
            desired_filename = add_datetime(desired_filename+".txt", '%Y%m%d_%H-%M-%S')
        else:
            desired_filename = add_datetime(desired_filename+".csv", '%Y%m%d_%H-%M-%S')

        try:

            if is_json:
                with open(desired_filename, 'w+') as jsonfile:
                    json.dump(find_files(desired_path), jsonfile, indent=2)
                zip_output(desired_filename)
            else:
                with open(desired_filename, 'w+', newline='') as csvfile:
                    fieldnames_csv = ['parent path', 'filename', 'filesize', 'md5', 'sha1']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames_csv)
                    writer.writeheader()

                    for lines in find_files(desired_path):
                        writer.writerow(lines)
                zip_output(desired_filename)

        except Exception as e:
            logger.error('Error: ' + str(e),exc_info=True)
    else:
        print("Path not found")


def main():

    config = configparser.ConfigParser()
    conf_dir = os.path.join(os.path.dirname(__file__), 'conf.ini')
    config.read(conf_dir)
    directory = config['args']['directory']
    filename = config['args']['filename']

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs='?', default=directory)
    parser.add_argument("csv_name", nargs='?', default=filename)
    parser.add_argument("-j", "--json", action="store_true")
    args = parser.parse_args()

    directory_to_csv(os.path.abspath(args.directory), args.csv_name, args.json)


if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)
    main()
