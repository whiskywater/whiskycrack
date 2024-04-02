Thank you for using whiskycrack. Below is a list of attributes used from the command line to help generate word lists.

USAGE: python whiskycrack.py

-l specifies length of each entry
-w specifies if words should be used (-l does not work with -w, just specify -l as "-l 0" or any number)
-f specifies the output file
-n specifies if numbers should be included
-c specifies if capitol numbers should be included
-s specifies if special characters should be included.

Ex.
python whiskycrack.py -l 3 -n -c -s -f wordlist.txt
python whiskycrack.py -l 0 -w cat dog frog -f wordlist.txt
