import glob
import os
import csv
import argparse


def directory_to_csv(desired_path, desired_filename):
    """Accepts a desired path and a desired filename,
    then use the directory to recursively collect data then print in a csv file.
    Args:
        desired_path : the directory to be processed
        desired_filename : the filename of the csv to be created
    """
    if os.path.exists(desired_path):
        with open(desired_filename, 'w+', newline='') as csvfile:
            fieldnames_csv = ['parent path', 'filename', 'filesize']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_csv)
            writer.writeheader()

            for root, directories, files in os.walk(desired_path):

                for file in files:
                    file_dict = {"parent path": os.path.dirname(root), "filename": file,
                                 "filesize": os.path.getsize("{}\{}".format(root, file))}
                    writer.writerow(file_dict)

    else:
        print("Path not found")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("csv_name")
    args = parser.parse_args()

    directory_to_csv(args.directory, args.csv_name)

