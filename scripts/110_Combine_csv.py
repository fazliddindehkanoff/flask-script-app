import os
import glob
from datetime import datetime
import pandas as pd

path='C:/Users/Public/Documents/Insomnia Sliki/Files'
csv_files=glob.glob(os.path.join(path,"*.csv"))
#print(csv_files)
#print(len(csv_files))

#DENESNA DATA VO IMETO NA FAJLOT
now = datetime.now()
name_time = now.strftime("%Y/%m/%d")
name_time=name_time.replace('/','_')
name_time=name_time.replace(':','-')
print(name_time)

#PATEKA DO KAJ SE FAJLOVITE
path='C:/Users/Public/Documents/Insomnia Sliki/Files'
files=os.listdir(path)
#print(files)
#print(len(files))

#LISTA NA SITE NAJNOVI FAJLOVI OD TEKOVEN DEN
LastFiles=[]
for i in csv_files:
    #print(i)
    if name_time in i: #smeni so name_time
        if 'Template' in i:
            print(i)
            LastFiles.append(i)
#print(LastFiles)

#KREIRANJE NA NOV ZBIREN CSV
filename=name_time+'_Setec'+'.csv'
filepath = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(filename)) 
if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
    os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')


print(filename)
for file in LastFiles:
    df = pd.read_csv(file)

    #print(df) 
#data=pd.DataFrame(columns=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Memmory Type','Capacity','GPU','Video Memmory','Screen Size','Refresh Rate','Motherboard','CPU','RAM','SSD','HDD','PSU','CPU Cooler','Case','Bazna Frekvencija','Maksimalna bust frekvencija','Broj na fizicki jadra','Broj na logicki jadra','L3 kes memorija','Arhitektura','TDP','Procesor','RAM memorija','Graficka karticka','Operativen sistem','Garancija','Socket - leziste','Chipset','RAM type','RAM DIMMs','USB 3.1 ports','m.2','SATA','Frekvencija','Interfejt','Kapacitet','Izdrzlivost - TBW','Sifra na artikl','Sifra'])
data=pd.DataFrame()
for file in LastFiles:    
    csv_data = pd.read_csv(file)
    #print(csv_data)
    data_partial = pd.DataFrame(csv_data, columns=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Garancija','Sifra na artikl','Sifra','BrendID','KategorijaID','Kategorija'])
    #POVEKJE OD 100 POENI DOSTAPNOST
    data_100poeni = data_partial.loc[pd.to_numeric(data_partial['Stock'], errors='coerce').fillna(0).ge(0)]

    #data_100poeni = data_partial.loc[data_partial['Weight']>=0]
    #data=pd.concat([data_100poeni],ignore_index=True, sort=False)
    #print(data_100poeni)
    #print(data)
    
    #data=data.append(data_100poeni,ignore_index=True)
    data=pd.concat([data,data_100poeni])
    #print(data_100poeni)
    print(data)
    data.to_csv(filepath,index=False)
    
    # csv_data = pd.read_csv(file)
    # #print(csv_data)
    # data_partial = pd.DataFrame(csv_data, columns=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Garancija','Sifra na artikl','Sifra','BrendID','KategorijaID','Kategorija'])
    # #POVEKJE OD 100 POENI DOSTAPNOST
    # data_100poeni = data_partial.loc[pd.to_numeric(data_partial['Weight'], errors='coerce').fillna(0).ge(1)]

    # #data_100poeni = data_partial.loc[data_partial['Weight']>=0]
    # #data=pd.concat([data_100poeni],ignore_index=True, sort=False)
    # #print(data_100poeni)
    # #print(data)
    
    # #data=data.append(data_100poeni,ignore_index=True)
    # data=pd.concat([data,data_100poeni])
    # #print(data_100poeni)
    # print(data)
    # data.to_csv(filepath,index=False)
    # #with open (filename,'w',encoding='utf8',newline='') as f:
    # #    writer= csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # #    writer(data_100poeni)


# print('Koregiranje na fajlot - Brend i Sifra')
# time.sleep(10)

# with open(filepath, 'r', newline='',encoding='utf8') as file:
#     reader = csv.reader(file)
#     data = [row for row in reader]

# #PROVERKA DALI VO SIFRI IMA TEXT
# for row in data[1:]:
#     try:
#         float(row[58])
#     except ValueError:
#         row[58] = '0'
# for row in data[1:]:
#     try:
#         float(row[57])
#     except ValueError:
#         row[57] = '0'

# #PROVERKA DALI BREND E PRAZNO
# for row in data:
#     if row[1] == '':
#         row[1] = 'XXX'

# with open(filepath, 'w', newline='', encoding='utf8') as file:
#     writer = csv.writer(file)
#     writer.writerows(data)