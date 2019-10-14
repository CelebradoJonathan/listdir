import os
import csv
import argparse
import hashlib
import zipfile


def zip_output(filename):
    """Accepts a desired filename,
        then zips that file.
        Args:
            filename : the filename of the zip file to be created
    """
    zip_name = filename + ".zip"
    with zipfile.ZipFile(zip_name, 'w') as out_zip:
        out_zip.write(filename)


def directory_to_csv(desired_path, desired_filename):
    """Accepts a desired path and a desired filename,
    then use the directory to recursively collect data then print in a csv file.
    Args:
        desired_path : the directory to be processed
        desired_filename : the filename of the csv to be created
    """
    if os.path.exists(desired_path):
        md5_hasher = hashlib.md5()
        sha1_hasher = hashlib.sha1()

        with open(desired_filename, 'w+', newline='') as csvfile:
            fieldnames_csv = ['parent path', 'filename', 'filesize', 'md5', 'sha1']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_csv)
            writer.writeheader()

            for root, directories, files in os.walk(desired_path):

                for file in files:
                    filepath = "{}\{}".format(root, file)

                    with open(filepath, 'rb') as afile:
                        buf = afile.read()
                        md5_hasher.update(buf)
                        sha1_hasher.update(buf)

                        file_dict = {"parent path": os.path.dirname(root), "filename": file,
                                     "filesize": os.path.getsize(filepath), "md5": md5_hasher.hexdigest(),
                                     "sha1": sha1_hasher.hexdigest()}

                        writer.writerow(file_dict)

        zip_output(desired_filename)

    else:
        print("Path not found")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("csv_name")
    args = parser.parse_args()

    directory_to_csv(args.directory, args.csv_name)
