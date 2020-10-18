import re
import csv

# open your csv and read as a text string
with open('my_new_csv.csv', 'r') as f:
    my_csv_text = f.read()

with open("my_new_csv.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for lines in csv_reader:
    	lineFive = lines[5]
    	print(lineFive[-4:])



find_str = '\( \)'




replace_str = ' '

# substitute
new_csv_str = re.sub(find_str, replace_str, my_csv_text)

# open new file and save
new_csv_path = './my_new_csv.csv' # or whatever path and name you want
with open(new_csv_path, 'w') as f:
    f.write(new_csv_str)

