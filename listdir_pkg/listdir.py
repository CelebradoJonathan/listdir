import os
import csv
import argparse
import hashlib
import zipfile
import configparser
import datetime


def zip_output(filename):
    """Accepts a desired filename,
    then zips that file.
        Args:
            filename : the filename of the zip file to be created
    """
    zip_name = filename + ".zip"
    with zipfile.ZipFile(zip_name, 'w') as out_zip:
        out_zip.write(filename)


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
            return sha1_hasher.hexdigest()
        elif hash_type == "md5":
            md5_hasher = hashlib.md5()
            md5_hasher.update(buf)
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
    return str_date + "_" + file_name


def directory_to_csv(desired_path, desired_filename):
    """Accepts a desired path and a desired filename,
    then use the directory to recursively collect data then print in a csv file.
    Args:
        desired_path : the directory to be processed
        desired_filename : the filename of the csv to be created
    """
    if os.path.exists(desired_path):
        desired_filename = add_datetime(desired_filename, '%Y%m%d_%H-%M-%S')
        with open(desired_filename, 'w+', newline='') as csvfile:
            fieldnames_csv = ['parent path', 'filename', 'filesize', 'md5', 'sha1']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_csv)
            writer.writeheader()

            for root, directories, files in os.walk(desired_path):

                for file in files:
                    file_path = "{}\{}".format(root, file)

                    file_dict = {"parent path": os.path.dirname(root), "filename": file,
                                 "filesize": os.path.getsize(file_path), "md5": get_hash(file_path, "md5"),
                                 "sha1": get_hash(file_path, "sha1")}

                    writer.writerow(file_dict)

        zip_output(desired_filename)

    else:
        print("Path not found")


def main():

    config = configparser.ConfigParser()
    conf_dir = os.path.dirname(__file__)
    config.read(conf_dir + "/conf.ini")
    directory = config['args']['directory']
    filename = config['args']['filename']

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs='?')
    parser.add_argument("csv_name", nargs='?')
    args = parser.parse_args()

    if args.directory and args.csv_name:
        directory_to_csv(args.directory, args.csv_name)
    else:
        directory_to_csv(directory, filename)


if __name__ == '__main__':
    main()