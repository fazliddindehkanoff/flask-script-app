import csv
import os
from datetime import datetime
import time



#FIND TWO LATEST SETEC FILES 
# 
# Set the directory where the CSV files are located
csv_directory = 'C:/Users/Public/Documents/Insomnia Sliki/Files/'

# Find all files in the directory
all_files = os.listdir(csv_directory)

# Filter out files that are not CSV or have a name length other than 10
csv_files = [f for f in all_files if f.endswith('.csv') and len(f[:-4]) == 16]

# Sort the CSV files by modification time, most recent first
csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(csv_directory, x)), reverse=True)

# Get the two most recent CSV files
latest_csv_files = csv_files[:2]

# Print the names of the two latest CSV files
print('The two latest CSV files with a name length of 16 (YYYY_MM_DD_Setec.csv) are:')
for csv_file in latest_csv_files:
    print(csv_file) 


#CREATE FULL PATH FOR LATEST SETEC FILES
# Set the paths of the two CSV files STAR i NOV
star_csv_path = "C:/Users/Public/Documents/Insomnia Sliki/Files/"+latest_csv_files[1]
print('STAR FILE',star_csv_path)
nov_csv_path = "C:/Users/Public/Documents/Insomnia Sliki/Files/"+latest_csv_files[0]
print('NOV FILE',nov_csv_path)






#PRINT ADDED AND DELETED VALUES FROM FILES 
#ADDED - NOVI (gi nema vo stariot gi ima vo noviot)
#DELETED - NEPOSTOECKI (gi ima vo stariot gi nema vo noviot)

# Open the Star.csv file and read the values in the 5th column into a set
# with open(star_csv_path,newline='',encoding='utf8') as star_file:
#     star_reader = csv.reader(star_file)
#     star_set = set(row[4] for row in star_reader)

# # Open the Nov.csv file and compare the values in the 5th column to the set
# with open(nov_csv_path,newline='',encoding='utf8') as nov_file:
#     nov_reader = csv.reader(nov_file)
#     for row in nov_reader:
#         if row[4] not in star_set:
#             print(f"Added: {row[4]}")

# # Compare the set to the values in the Nov.csv file to find any deleted values
# for value in star_set:
#     with open(nov_csv_path,newline='',encoding='utf8') as nov_file:
#         nov_reader = csv.reader(nov_file)
#         if value not in (row[4] for row in nov_reader):
#             print(f"Deleted: {value}")


#IMINJA NA NOVITE FAJLOVI
now = datetime.now()
dt_string = now.strftime("%Y/%m/%d")
dt_string=dt_string.replace('/','_')
dt_string=dt_string.replace(':','-')
NepostoeckiName=dt_string+'_Nepostoecki_Setec.csv'
NoviName=dt_string+'_Novi_Setec.csv'

nepostoecki_file_path = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(NepostoeckiName))
if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
    os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')

novi_file_path = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(NoviName))
if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
    os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')


#ZAPISUVA VO POSEBNI FAJLOVI


# Open the Star.csv file and read the values in the 5th column into a set
with open(star_csv_path,newline='',encoding='utf8') as star_file:
    star_reader = csv.reader(star_file)
    star_set = set(row[4] for row in star_reader)

# Open the Nov.csv file and compare the values in the 5th column to the set
added_rows = []
with open(nov_csv_path,newline='',encoding='utf8') as nov_file:
    nov_reader = csv.reader(nov_file)
    for row in nov_reader:
        if row[4] not in star_set:
            added_rows.append(row)

# Write added rows to a CSV file
with open(novi_file_path, 'w',newline='',encoding='utf8') as added_file:
    writer = csv.writer(added_file)
    header=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Garancija','Sifra na artikl','Sifra','BrendID','KategorijaID','Kategorija']
    writer.writerow(header)
    writer.writerows(added_rows)

# Compare the set to the values in the Nov.csv file to find any deleted rows
deleted_rows = []
with open(star_csv_path,newline='',encoding='utf8') as star_file:
    star_reader = csv.reader(star_file)
    for row in star_reader:
        if row[4] not in (nov_row[4] for nov_row in csv.reader(open(nov_csv_path,newline='',encoding='utf8'))):
            deleted_rows.append(row)

# Write deleted rows to a CSV file
with open(nepostoecki_file_path, 'w',newline='',encoding='utf8') as deleted_file:
    writer = csv.writer(deleted_file)
    header=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Garancija','Sifra na artikl','Sifra','BrendID','KategorijaID','Kategorija']
    writer.writerow(header)
    writer.writerows(deleted_rows)
