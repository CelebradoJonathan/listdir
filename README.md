# listdir
This program accepts a desired path and a desired filename, then use the directory to recursively collect data then print in a csv file.

To run the program: open the terminal, then go to the directory of the file then type : "python listdir.py <directory> <filename>"


Note: If the program encounters an inaccessible file the csv file will stop printing in that particular file. Sorry for the inconvinience, 
I'll fix this as soon as I know how to. 

usage: listdir.py [-h] [-j] [-c] [-q] [directory] [csv_name]

positional arguments:
  directory    the directory to be recursively checked
  csv_name     the desired file name

optional arguments:
  -h, --help   show this help message and exit
  -j, --json   option to make the output a json
  -c, --csv    option to make the output a csv
  -q, --query  option to make the output save in the database

