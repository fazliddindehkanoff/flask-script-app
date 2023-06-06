import os
from datetime import datetime
import csv

folder_path = "data"
              
#list of all files in the folder
folder_file_list = os.listdir(folder_path)

fixed_file_list=[]

#napravi lista od denesni fajlovi
kategorii=['Graficki','Laptopi','HardDisk','Procesori','RAM','MaticniPloci','Kuleri','Kukista','Napojuvanja','Konfiguracii','Monitori','Tastaturi','Gluvci','WebKameri','LaptopDopolnitelna','OptickiUredi','TVZvucni','Pecatari','Skeneri','Slusalki','EksterniDiskovi','USBMemorii','MemoriskiKarticki','Multimedia','KompjuterskiDodatoci']
now=datetime.now()
dt_string = now.strftime("%Y/%m/%d")
dt_string=dt_string.replace('/','_')
dt_string=dt_string.replace(':','-')
#dt_string='2023_02_21' #------------------------------------BRISI POSLE TEST
for kat in kategorii:
    fixed_file_list.append(dt_string+'_Setec_'+kat+'_Template'+'.csv')
    #PRODOLZI TUKA!!!!!!
print('vo folder:',folder_file_list)
print('vo folder:',len(folder_file_list))
print('vo skripta',fixed_file_list)
print('vo skripta:',len(fixed_file_list))

nedostigaat=[]
denesni=[]
for site in folder_file_list:
    if site[:10]==dt_string:
        denesni.append(site)
        #print(site)
print('DENESNI',denesni)
print('Denesni',len(denesni))

FALAT=[]
FALAT=set(fixed_file_list)-set(denesni)
             
print("FALAT",FALAT)
print('FALAT',len(FALAT))

skripta=[]
for x in list(FALAT):
    if 'Graficki' in x:
        skripta.append('1')
    elif 'HardDisk'in x:
        skripta.append('2')
    elif 'Laptopi'in x:
        skripta.append('3')
    elif 'Procesori'in x:
        skripta.append('4')
    elif 'RAM'in x:
        skripta.append('5')
    elif 'MaticniPloci'in x:
        skripta.append('6')
    elif 'Kuleri'in x:
        skripta.append('7')
    elif 'Kukista'in x:
        skripta.append('8')
    elif 'Napojuvanja'in x:
        skripta.append('9')
    elif 'Konfiguracii'in x:
        skripta.append('10')
    elif 'Monitori'in x:
        skripta.append('11')
    elif 'Tastaturi'in x:
        skripta.append('12')
    elif 'Gluvci'in x:
        skripta.append('13')
    elif 'WebKameri'in x:
        skripta.append('14')
    elif 'LaptopDopolnitelna'in x:
        skripta.append('15')
    elif 'OptickiUredi'in x:
        skripta.append('16')
    elif 'TVZvucni'in x:
        skripta.append('17')
    elif 'Pecatari'in x:
        skripta.append('18')
    elif 'Skeneri'in x:
        skripta.append('19')
    elif 'Slusalki'in x:
        skripta.append('20')
    elif 'EksterniDiskovi'in x:
        skripta.append('21')
    elif 'USBMemorii'in x:
        skripta.append('22')
    elif 'MemoriskiKarticki'in x:
        skripta.append('23')
    elif 'Multimedia'in x:
        skripta.append('24')
    elif 'KompjuterskiDodatoci'in x:
        skripta.append('25')
    
    

if len(list(FALAT))!=0:
    for z in FALAT:
        print('Fali: ',z)
    for c in skripta:
        print('Setec skripta: = ',c)
    falat_kodovi=list(skripta)
    print(falat_kodovi)
    falat_kodovi1=[]
    for i in skripta:
        falat_kodovi1.append(int(i))
    print(falat_kodovi1)
    #falat_kodovi1=[eval(i) for i in skripta]
    #print(falat_kodovi.sort(key=int))
    #falat_kodovi1=falat_kodovi.sort(key=int)
    #print(falat_kodovi1)

    #IME NA FAJLOT DATUM_NEIZVRSENI.csv
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d")
    dt_string=dt_string.replace('/','_')
    dt_string=dt_string.replace(':','-')
    Ime=dt_string+'_Neizvrseni_Skripti.csv'

    ime_path= os.path.join(folder_path,str(Ime))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    with open(ime_path, 'w',newline='',encoding='utf8') as f:
        writer = csv.writer(f,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        header=['Neizvrseni']
        writer.writerow(header)
        writer.writerow(falat_kodovi1)

