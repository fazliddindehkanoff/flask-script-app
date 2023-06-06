from bs4 import BeautifulSoup
import requests
from os import path
from abc import abstractproperty
from requests_html import HTMLSession
import urllib.request
import os
import csv
from datetime import datetime
import time
#import Funkcii_za_Struktura_v1

s=HTMLSession()


                                                                                                #SITE FUNKCII DA PRIMAAT SOUP?????
                                                                                                #POSEBNA FUNKCIJA DA DOBIVA SOUP I TRY/EXCEPT
                                                                                                #

#LISTA OD KATEGORII NA SETEC (Link,Ime)
KategoriiLinks=[#['https://setec.mk/index.php?route=product/category&path=10002_10003&limit=100','Laptopi'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10025&limit=100','Graficki'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10023&limit=100','HardDisk'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10021&limit=100','Procesori'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10024&limit=100','RAM'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10022&limit=100','MaticniPloci'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10027&limit=100','Kuleri'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10028&limit=100','Kukista'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10029&limit=100','Napojuvanja'],
#['https://setec.mk/index.php?route=product/category&path=10019_10032&limit=100','Konfiguracii'],                        #LIMIT=100 dali treba da stoi? da se proveri kako funkcioni so i bez
#['https://setec.mk/index.php?route=product/category&path=10019_10031&limit=100','Monitori'],
#['https://setec.mk/index.php?route=product/category&path=10019_10038_10040&limit=100','Tastaturi'],
#['https://setec.mk/index.php?route=product/category&path=10019_10038_10039&limit=100','Gluvci'],
['https://setec.mk/index.php?route=product/category&path=10019_10038_10041&limit=100','WebKameri'],
#['https://setec.mk/index.php?route=product/category&path=10002_10005&limit=100','LaptopDopolnitelna'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10026&limit=100','OptickiUredi'],
#['https://setec.mk/index.php?route=product/category&path=10019_10020_10030&limit=100','TVZvucni'],
##['https://setec.mk/index.php?route=product/category&path=10019_10038_10042&limit=100','PrenosniKutii'],
#['https://setec.mk/index.php?route=product/category&path=10019_10033&limit=100','Pecatari'],
#['https://setec.mk/index.php?route=product/category&path=10019_10035&limit=100','Skeneri'],
##['https://setec.mk/index.php?route=product/category&path=10019_10036&limit=100','Toneri'],
##['https://setec.mk/index.php?route=product/category&path=10019_10037&limit=100','MreznaOprema'],
#['https://setec.mk/index.php?route=product/category&path=10019_10043&limit=100','Slusalki'],
#['https://setec.mk/index.php?route=product/category&path=10019_10047&limit=100','EksterniDiskovi'],
#['https://setec.mk/index.php?route=product/category&path=10019_10044&limit=100','USBMemorii'],
#['https://setec.mk/index.php?route=product/category&path=10019_10045&limit=100','MemoriskiKarticki'],
##['https://setec.mk/index.php?route=product/category&path=10019_10051&limit=100','KabliKonektori'],
#['https://setec.mk/index.php?route=product/category&path=10019_10053&limit=100','Multimedia'],
#['https://setec.mk/index.php?route=product/category&path=10019_10223&limit=100','KompjuterskiDodatoci'],
#['https://setec.mk/index.php?route=product/category&path=10019_10046&limit=100','Software']
]

print(KategoriiLinks)

#AVTOMATSKO BARANJE BROJ NA STRANI
def get_strani(url,kategorija):
    r=s.get(url)
    soup = BeautifulSoup(r.text, 'lxml') 

    if  soup.find('div',class_='col-sm-6 text-right'):
        strani_text=soup.find('div',class_='col-sm-6 text-right')
        strani_text=strani_text.get_text().strip()
    #print(strani_text)
    
        #NAOGA BROJKA NA STRANI VO STRING
        txt=strani_text.split('(')
        for p in txt[1]:
            if p.isnumeric():
                z=p                                                                 #DA PREPOZNAVA DVOCIFREN BROJ NA STRANI (MREZNA OPREMA)------------------------------------------------------------
    else:
        z=0
    print('Pronajdeni se vkupno strani:',z,' od kategorija:',kategorija)
    return z


url_pages=[]

#KREIRANJE LINKOVI ZA SEKOJA STRANA
def pages_link(OsnovenLink,Strani):
    url_pagesf=[]
    if Strani!=0:
        urlbase=OsnovenLink
        urlbase2=urlbase+'&page='
        for strana in range(1,int(Strani)+1):
            #print('ALOO',strana)
            url_pagesf.append(urlbase2+str(strana))
            #print(url_pagesf)
    else:
        url_pagesf=['NEMA']
    return url_pagesf
#print('ZZZ',pages_link('https://setec.mk/index.php?route=product/category&path=10019_10031&limit=100',5))

#LINKOVI DO SEKOJ PROIZVOD NA STRANATA
def get_links(url):
    r=s.get(url)
    #time.sleep(2.5)
    items=r.html.find('div.image')                              #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
    links=[]
    for item in items:
        links.append(item.find('a',first=True).attrs['href'].strip())
    return links

#IME NA PRODUKT IME NA ARTIKL
def get_product_name(link):
    r=s.get(link)
    #print(r)
    #IME NA PRODUKTOT
  #  if r.html.find('h1',first=True).full_text.strip():          #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
   #     ArtiklIME=r.html.find('h1',first=True).full_text.strip()
   # else:
   #     ArtiklIME="None"
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    if soup.find('h1',id='title-page'):
        ArtiklIME=soup.find('h1',id='title-page')
        ArtiklIME=ArtiklIME.get_text().strip()
    else:
        ArtiklIME="NaN"

    return ArtiklIME

#HTML OPIS NA ARTIKL
def get_opis_html(link):
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    if soup.find('div',id='tab-description'):                         #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
        Opis1_html=soup.find('div',id='tab-description')
        #print(Opis1_html)
        Opis1_html=str(Opis1_html)
        Opis_html=Opis1_html.replace(',','<br>')
        
        #print(Opis1_html)
        #Opis_html=Opis1_html.get_text()
        #Opis_html=Opis_html.replace(',',' ')
        #Opis_html=Opis_html.split(',')
    
    return Opis_html



#OPIS NA ARTIKL
def get_opis(link):
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    if soup.find('div',id='tab-description'):                         #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
        Opis1=soup.find('div',id='tab-description')
        Opis=Opis1.get_text().strip()
        Opis=Opis.replace(' - ',',')
        Opis=Opis.split(',')
    
    return Opis

#DOSTAPNOST PO SALONI
def Get_dostapnost(link):
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')                  #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
    #LOGIKA AKO NEMA SPECIFIKACIJA (DOSTAPNOST)
    if  soup.find('div',id='tab-attribute'):
        Dostapnost1=soup.find('div',id='tab-attribute')
        Dostapnost1=Dostapnost1.get_text().strip()
    else:
        Dostapnost1='NaN'
    Dostp=Dostapnost1.replace('Напреден Филтер','')
    Dostp2=Dostp.replace('Достапност по салони','')
    Dostp2=Dostp2.replace('   ','')
    Dostapnost=list(Dostp2.split("Сетек"))
    Dostapnost=Dostapnost[1:]
    return Dostapnost


#POENI OD DOSTAPNOST
def get_poeni(link):
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')                      #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
    if  soup.find('div',id='tab-attribute'):
        Dostapnost1=soup.find('div',id='tab-attribute')
        Dostapnost1=Dostapnost1.get_text().strip()
    else:
        Dostapnost1='NaN'
    Dostp=Dostapnost1.replace('Напреден Филтер','')
    Dostp2=Dostp.replace('Достапност по салони','')
    Dostp2=Dostp2.replace('   ','')

    Dostp2.replace(" ","")
    Dostp2.replace("' Рузвелтова '","Ruzveltova")
    Dostp2.replace(' ГТЦ ИТ ','GTC_IT')
    #print(Dostp2)
    dostaprevod=Dostp2.split("Сетек")
    #print(dostaprevod)
    GlavenMagacinPoeni=RuzveltovaPoeni=CityMallPoeni=GTC_ITPoeni=GTC_HINNPoeni=StadionPoeni=AerodromPoeni=GPetrovPoeni=CairPoeni=SVNikolePoeni=RadovisPoeni=StrugaPoeni=PrilepPoeni=GostivarPoeni=TetovoPoeni=BitolaPoeni=KavadarciPoeni=GevgelijaPoeni=ResenPoeni=DebarPoeni=OhridPoeni=Ohrid2Poeni=StipPoeni=KumanovoPoeni=StrumicaPoeni=KocaniPoeni=VelesPoeni=KicevoPoeni=KPalankaPoeni=DelcevoPoeni=0
    for alo in dostaprevod:
        alo=alo.strip()
        #print(alo)
        if alo=="Рузвелтова":
            RuzveltovaPoeni=2
        elif alo=='Сити Мол':
            CityMallPoeni=2
        elif alo=='ГТЦ ИТ':
            GTC_ITPoeni=2
        elif alo=='ГТЦ до Холидеј Ин':
            GTC_HINNPoeni=2
        elif alo=='Стадион':
            StadionPoeni=2
        elif alo=='Аеродром':
            AerodromPoeni=2
        elif alo=='Ѓорче Петров':
            GPetrovPoeni=2
        elif alo=='Чаир':
            CairPoeni=2
        elif alo=='Свети Николе':
            SVNikolePoeni=1
        elif alo=='Радовиш':
            RadovisPoeni=1
        elif alo=='Струга':
            StrugaPoeni=1
        elif alo=='Прилеп':
            PrilepPoeni=1
        elif alo=='Гостивар':
            GostivarPoeni=1
        elif alo=='Тетово':
            TetovoPoeni=1
        elif alo=='Битола':
            BitolaPoeni=1
        elif alo=='Кавадарци':
            KavadarciPoeni=1
        elif alo=='Гевгелија':
            GevgelijaPoeni=1
        elif alo=='Ресен':
            ResenPoeni=1
        elif alo=='Дебар':
            DebarPoeni=1
        elif alo=='Охрид':
            OhridPoeni=1
        elif alo=='Охрид 2':
            Ohrid2Poeni=1
        elif alo=='Штип':
            StipPoeni=1
        elif alo=='Куманово':
            KumanovoPoeni=1
        elif alo=='Струмица':
            StrumicaPoeni=1
        elif alo=='Кочани':
            KocaniPoeni=1
        elif alo=='Велес':
            VelesPoeni=1
        elif alo=='Кичево':
            KicevoPoeni=1
        elif alo=='Крива Паланка':
            KPalankaPoeni=1
        elif alo=='Делчево':
            DelcevoPoeni=1
    if soup.find('div',class_='col-lg-4 col-md-4 col-sm-4 col-xs-4'):
        glaven=soup.find('div',class_='col-lg-4 col-md-4 col-sm-4 col-xs-4')   #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
        glaven=glaven.find('img',src=True)
        glaven=glaven['src']
        #print('GLAVEN',glaven)
    if glaven=='image/no.png':
        #print('NEMA VO GLAVEN MAGACIN -----------------------------------')
        GlavenMagacinPoeni=0
    elif glaven=='image/yes.png':
        #print('IMA VO GLAVEN MAGACIN ++++++++++++++++++++++++++++++++++++')
        GlavenMagacinPoeni=100

    POENI=GlavenMagacinPoeni+RuzveltovaPoeni+CityMallPoeni+GTC_ITPoeni+GTC_HINNPoeni+StadionPoeni+AerodromPoeni+GPetrovPoeni+CairPoeni+SVNikolePoeni+RadovisPoeni+StrugaPoeni+PrilepPoeni+GostivarPoeni+TetovoPoeni+BitolaPoeni+KavadarciPoeni+GevgelijaPoeni+ResenPoeni+DebarPoeni+OhridPoeni+Ohrid2Poeni+StipPoeni+KumanovoPoeni+StrumicaPoeni+KocaniPoeni+VelesPoeni+KicevoPoeni+KPalankaPoeni+DelcevoPoeni
    return POENI


#REDOVNA I KLUB CENA
def get_cena(link):
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')                    #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
    if r.html.find('span.price-old-product') and r.html.find('div.onlinecena span'):
        RedovnaCena=soup.find('span',id='price-old-product')
        RedovnaCena=RedovnaCena.get_text().strip()
        KlubCena=soup.find('span',id='price-special')
        KlubCena=KlubCena.get_text().strip()
        #print('IMA REDOVNA I KLUB CENA')

    else: # Ako nema Klub cena braj samo Redovna RABOTI SO KIRILICA 
        KlubCena="NaN"
        #soup = BeautifulSoup(r.text, 'lxml')
        RedoCena=soup.find('div',id='price-old')
        RedovnaCena=RedoCena.get_text().strip()
        #print('IMA SAMO REDOVNA CENA')
    return RedovnaCena,KlubCena

#GARANCIJA
def get_garancija(link):
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    if soup.find("div", class_="description"):                            #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
        brendsifra=soup.find("div", class_="description")
        celo=brendsifra.get_text().strip()                                  #GARANCIJA 90 dena SREDI GO----------------------------------------------------------------------
        #print(celo)
        #GARANCIJA
        Garancija=celo[-4:]
        Garancija.replace(':','')

    return Garancija

#SIFRA
def get_sifra(link):
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')                            #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
    if soup.find("div", class_="description"):
        brendsifra=soup.find("div", class_="description")
        celo=brendsifra.get_text().strip()
        #print(celo)
        #GARANCIJA
        Garancija=celo[-4:]
        Garancija.replace(':','')

        list1 =list(celo.split(":"and" "))
        Sifra1=list1[-4:]
        Sifra=Sifra1[0]
        #print('SIFRA=',Sifra)
    if Sifra=='':                                                         #https://setec.mk/index.php?route=product/product&path=10019_10031&product_id=27670&limit=100
        linkk=link[-15:]
        Sifra=linkk[:5]

    return Sifra

#MODEL
def get_model(link):
    r=s.get(link)
    soup = BeautifulSoup(r.text, 'lxml')                                #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
    brendsifra=soup.find("div", class_="description")
    celo=brendsifra.get_text().strip()
    #print(celo)
    #GARANCIJA
    Garancija=celo[-4:]
    Garancija.replace(':','')

    list1 =list(celo.split(":"and" "))
    Sifra1=list1[-4:]
    Sifra=Sifra1[0]
    #print('SIFRA=',Sifra)
    
    KOpis=list1[4:-8]
    MODEL=''
    for x in KOpis:
        MODEL+=' '+x
    #print('MODEL:',MODEL)
    
    return MODEL


#BREND
def get_brend(link):
    r=s.get(link)
    if r.html.find('div.description'):
        listaBrend=r.html.find('div.description') #Brend                           #PROBAJ SO TRY EXCEPT ZA DA IZBEGNIS ERROR=======================================
        for item in listaBrend:
            Brend.append(item.find('a',first=True).full_text.strip())
    return Brend


#A      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#K      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#T      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#I      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#V      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#A      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#C      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#I      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#J      AKTIVACIJA                    -------------------------------------------------------------------------------------------------
#A      AKTIVACIJA                    -------------------------------------------------------------------------------------------------



#AKTIVACIJA NA KATEGORII, PAGES_LINK I GET_STRANI, SCRAPING FUNKCII
for Kategorija in range(0,len(KategoriiLinks)):
    Kat=KategoriiLinks[Kategorija]
    #Link na kategorija
    LinkKat=Kat[0]
    #Ime na kategorija
    NameKat=Kat[1]
    #AKTIVIRAJ GET STRANI -naogja broj na strani od Kategorija
    Strani=0 #RESET POSLE SEKOJA KATEGORIJA
    Strani=get_strani(LinkKat,NameKat)
    print('Strani:',Strani)
    #AKTIVIRAJ PAGES LINK -kreira linkovi za pristap do sekoja strana od kategorija
    url_pages=[] #RESET POSLE SEKOJA KATEGORIJA
    url_pages.append(pages_link(LinkKat,Strani))
    url_pages=sum(url_pages,[])
    print('URL_PAGES po kategorija',NameKat,'---',url_pages)
    #LINKOVI DO SEKOJ PROIZVOD OD KATEGORIJA
    links_produkti=[]
    for page in url_pages:
        if page!='NEMA':
            #SEKOJ PROIZVOD PO STRANA OD KATEGORIJA
            links_produkti_strana=[]
            links_produkti_strana=get_links(page)

            links_produkti.append(links_produkti_strana)
            #print(links_produkti)
            print('Dolzina po strana:',len(links_produkti_strana))
            #print('Dolzina Links_produkti',len(links_produkti))
            #links_produkti=sum(links_produkti,[])

    #SITE PROIZVODI OD SITE STRANI PO KATEGORIJA        
    links_produkti=sum(links_produkti,[])
    print('Dolzina SITE strani',len(links_produkti))

    #DEFINICIJA NA LISTI ZA SEKOJA KATEGORIJA
    Reden_brojID=[] #se misli na reden broj od listata vo csv, nesto kako ID
    ArtiklIME=[] #glavno ime gore h1
    Brend=[] #brend od description
    Model=[] # Kratok Opis od description
    Sifra=[] #sifra od description                      5 cifri skogas
    Garancija=[] #grancija of description               posledni 2-3-4 cifri
    RedovnaCena=[] #Redovna cena od description
    KlubCena=[] #Klub cena od description
    Opis=[] #golem opis DOLU
    OpisHtml=[] #HTML OPIS
    Dostapnost=[] #od specifikacija DOLU


    #DEFINICIJA NA FINALNI LISTI ZA SEKOJA KATEGORIJA
    ArtiklIME=[]
    OpisOK=[]
    OpisHtmlOK=[]
    DostapnostOK=[]
    POENIOK=[]
    RedovnaCenaOK=[]
    KlubCenaOK=[]
    CenaOK=[]
    RedenBrojIDOK=[]
    GarancijaOK=[]
    SifraOK=[]
    ModelOK=[]
    BrendOK=[]
    #RedovnaCena2=[]
    Reden_brojID=1  #NAJDI LOGIKA ZA ID ZA SEKOJA KATEGORIJA

    for i in links_produkti: #smeni vo: for i in links_produkti:
        r=s.get(i)
        soup = BeautifulSoup(r.text, 'lxml')
        #IME NA ARTIKL 
        ArtiklIME.append(get_product_name(i))

        #REDEN BROJ ID interno
        #print('interno ID: ',Reden_brojID)

        r=s.get(i)
        soup = BeautifulSoup(r.text, 'lxml')
        
        OpisOK.append(get_opis(i))
        #print('OPISFUNKCIJA',OpisOK)

        OpisHtmlOK.append(get_opis_html(i))
        #print(OpisHtml)

        DostapnostOK.append(Get_dostapnost(i))
        #print('DOSTAPNOST FUNKCIJA',DostapnostOK)

        POENIOK.append(get_poeni(i))
        #print('POENI FUNKCIJA',POENIOK)
        
        CenaOK.append(get_cena(i))
        #print('CENA FUNCKIJA',CenaOK)

        #CENA OD TUPLES VO LIST OF LISTS
        CenaOK=list(map(list,CenaOK)) 

        RedenBrojIDOK.append(str(Reden_brojID))           #ID PO KATEGORIJA SMENI NA POCETOK ZA KRATENKA RAM/HDD/GPU....
        print('ID:',NameKat,Reden_brojID,i)
        Reden_brojID=Reden_brojID+1
        #print('INTERNO ID FUNKCIJA',RedenBrojIDOK)


        GarancijaOK.append(get_garancija(i))
        #print('Garancija funkcija',GarancijaOK)

        SifraOK.append(get_sifra(i))
        #print('Sifra funkcija',SifraOK)
    

        ModelOK.append(get_model(i))
        #print('Model Funkcija',ModelOK)

        BrendOK.append(get_brend(i))
        #print(Brend)

    #KONTROLA NA PRODUKTI
    print("Vkupno ID:",len(RedenBrojIDOK),'vo kategorija',NameKat)
    print("Vkupno Iminja",len(ArtiklIME),'vo kategorija',NameKat)
    print('Vkupno Opisi:',len(OpisOK),'vo kategorija',NameKat)
    print('Vkupno Dostapnost',len(DostapnostOK),'vo kategorija',NameKat)
    print('Vkupno ceni:',len(CenaOK),'vo kategorija',NameKat)
    print('Vkupno modeli',len(ModelOK),'vo kategorija',NameKat)
    print('Vkipno sifri',len(SifraOK),'vo kategorija',NameKat)
    print('Vkupno poeni:',len(POENIOK),'vo kategorija',NameKat)
    print('Vkupno garancii',len(GarancijaOK),'vo kategorija',NameKat)


    #IME NA FILE (DATUM I VREME)                              
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d")
    dt_string=dt_string.replace('/','_')
    dt_string=dt_string.replace(':','-')
    file=dt_string+'_Setec_'+NameKat+'.txt' #TEXT FILE ZA RACNO VNECUVANJE 
    file2=dt_string+'_Setec_'+NameKat+'_INFO'+'.csv' #CSV INFO FILE 
    file3=dt_string+'_Setec_'+NameKat+'_OPIS'+'.csv' #CSV OPIS FILE
    file4=dt_string+'_Setec_'+NameKat+'_SALONI'+'.csv'  #CSV SALONI FILE
    file5=dt_string+'_Setec_'+NameKat+'_ALL'+'.csv'  #CSV ALL FILE
    file6=dt_string+'_Setec_'+NameKat+'_Template'+'.csv' #INSOMNIA TEMPLATE
    print(file)
    print(file2)
    print(file3)
    print(file4)
    print(file5)
    print(file6)

    #KREIRANJE NA FILES VO FOLDER
    #TEXT FILE ZA RACNO VNESUVANJE
    # filepath = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(file)) #'C:/Users/simce/OneDrive - A.D. Mepso/MEPSO - OneDrive/14_APPs/Insomnia mk/files'
    # if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
    #     os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')
    # #INFO FILE CSV
    # filepath2 = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(file2))
    # if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
    #     os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')
    # #OPIS FILE CSV
    # filepath3 = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(file3))
    # if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
    #     os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')
    # #SALONI FILE CSV
    # filepath4 = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(file4))
    # if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
    #     os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')
    # #KOMPLETEN FILE CSV
    # filepath5 = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(file5))
    # if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
    #     os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')
    #MARTIN FILE
    filepath6 = os.path.join('C:/Users/Public/Documents/Insomnia Sliki/Files',str(file6))
    if not os.path.exists('C:/Users/Public/Documents/Insomnia Sliki/Files'):
        os.makedirs('C:/Users/Public/Documents/Insomnia Sliki/Files')

    #PISUVA VO TEXT FILE ZA RACNO VNESUVANJE
    # with open(filepath,'w',encoding='utf8',newline='') as textfile:
    #     #textfile = csv.writer(textfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     elementi=len(ArtiklIME)
    #     listaelementi=list(range(0,elementi))#elementi-1
    #     for i in listaelementi:
    #         textfile.write('------------------------------------> ')
    #         textfile.write(ArtiklIME[i])
    #         textfile.write(' <------------------------------------')
    #         textfile.write('\n')
    #         textfile.write('------>Sifra: ')
    #         textfile.write(SifraOK[i])

    #         textfile.write('<------>Garancija: ')
    #         textfile.write(GarancijaOK[i])
    #         textfile.write(' dena')
    #         textfile.write('<------>Brend: ')
    #         textfile.write(Brend[i])
    #         #PISUVAJ CENA
    #         textfile.write('<------>Redovna Cena: ')
    #         alo=CenaOK[i]
    #         textfile.write(alo[0])
    #         textfile.write('<------>Klub Cena: ')
    #         bla=CenaOK[i]
    #         textfile.write(bla[1])
    #         #PISUVAJ POENI
    #         textfile.write('<------>Poeni Dostapnost: ')
    #         textfile.write(str(POENIOK[i]))
            
    #         textfile.write('\n')
    #         textfile.write('------Kategorija: ')
    #         textfile.write(str(NameKat))

    #         textfile.write('\n')
    #         textfile.write('------Link: ')
    #         textfile.write(links_produkti[i])

    #         textfile.write('\n')
    #         textfile.write('------Interno ID: ')
    #         textfile.write(str(RedenBrojIDOK[i]))
    #         textfile.write('\n')
    #         textfile.write('------DOSTAPNOST saloni: ')
    #         for x in DostapnostOK[i]:
    #             textfile.write(x)
    #             textfile.write('\n')
    #             textfile.write('                         ')
    #         textfile.write('\n')
    #         textfile.write('------OPIS: ')
    #         for y in OpisOK[i]:
    #             textfile.write(y)
    #             textfile.write('\n')
    #             textfile.write('            ')    
    #         textfile.write('\n')
    #         textfile.write('')
    #         textfile.write('===========================================================================================================================================================')
    #         textfile.write('\n')

    # #PISUVA VO FILE INFO CSV
    # with open (filepath2,'w',encoding='utf8',newline='') as f:
    #     writer= csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     header=['Interno ID','Kategorija','Sifra','Ime','Redovna Cena','Klub Cena','Poeni Dostapnost','Garancija','Link']
    #     writer.writerow(header)
    #     elementi=len(ArtiklIME)
    #     listaelementi=list(range(0,elementi)) #elementi-1
    #     for i in listaelementi:
    #         c=CenaOK[i]
    #         c[0]=c[0].replace(',','')
    #         c[1]=c[1].replace(',','')
    #         c[0]=c[0].replace(' Ден','')
    #         c[1]=c[1].replace(' Ден','')
    #         c[1]=c[1].replace('.','')
    #         informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],ArtiklIME[i],c[0],c[1],POENIOK[i],GarancijaOK[i],links_produkti[i]]
    #         writer.writerow(informacii)

    # #PISUVA VO FILE OPIS CSV
    # with open (filepath3,'w',encoding='utf8',newline='') as f:
    #     writer= csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     header=['Interno ID','Kategorija','Sifra','Ime','Opis']
    #     writer.writerow(header)
    #     elementi=len(ArtiklIME)
    #     listaelementi=list(range(0,elementi)) #elementi-1
    #     for i in listaelementi:
            
    #         #KONVERZIJA OD LISTA VO STRING
    #         opis=OpisOK[i]
    #         opis2=''
    #         mesto=' ' #PROBAAJ SO TAB ili NESTO DRUGO ZA DA SE RAZDVOJAT VIZUELNO/EXCEL ======================== POVTORI GO ISTOTO ZA OPIS
    #         opis2=mesto.join(OpisOK[i])

    #         informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],ArtiklIME[i],opis2]
    #         #print('OPIS',informacii)
    #         writer.writerow(informacii)

    # #PISUVA VO FILE DOSTAPNOST SALONI
    # with open (filepath4,'w',encoding='utf8',newline='') as f:
    #     writer= csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     header=['Interno ID','Kategorija','Sifra','Salon']
    #     writer.writerow(header)
    #     #writer.write('\n')    #_csv.writer' object has no attribute 'write' -------------------------------------
    #     elementi=len(SifraOK)
    #     listaelementi=list(range(0,elementi)) #elementi-1
    #     #print(listaelementi)
    #     for i in listaelementi:
    #         #print(DostapnostOK[i])
    #         Salon=DostapnostOK[i]
    #         dolzina=len(DostapnostOK[i])
    #         if DostapnostOK[i]=='':
    #             DostapnostOK[i]='NaN'
            
    #         #KONVERZIJA OD LISTA VO STRING
    #         salon=DostapnostOK[i]
    #         salon2=''
    #         mesto=' ' #PROBAAJ SO TAB ili NESTO DRUGO ZA DA SE RAZDVOJAT VIZUELNO/EXCEL ======================== POVTORI GO ISTOTO ZA OPIS
    #         salon2=mesto.join(DostapnostOK[i])
    #         informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],salon2]
    #         #print(informacii)
    #         writer.writerow(informacii)
    
    
    # #PISUVA VO FILE ALL FILE
    # with open (filepath5,'w',encoding='utf8',newline='') as f:
    #     writer= csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     header=['Interno ID','Kategorija','Sifra','Ime','Redovna Cena','Klub Cena','Poeni Dostapnost','Garancija','Link','Opis','Salon']
    #     writer.writerow(header)
    #     #writer.write('\n')    #_csv.writer' object has no attribute 'write' -------------------------------------
    #     elementi=len(SifraOK)
    #     listaelementi=list(range(0,elementi)) #elementi-1
    #     #print(listaelementi)
    #     for i in listaelementi:
    #         #print(DostapnostOK[i])
    #         Salon=DostapnostOK[i]
    #         dolzina=len(DostapnostOK[i])
    #         if DostapnostOK[i]=='':
    #             DostapnostOK[i]='NaN'
            
    #         #KONVERZIJA OD LISTA VO STRING
    #         salon=DostapnostOK[i]
    #         salon2=''
    #         mesto=' ' #PROBAAJ SO TAB ili NESTO DRUGO ZA DA SE RAZDVOJAT VIZUELNO/EXCEL ======================== POVTORI GO ISTOTO ZA OPIS
    #         salon2=mesto.join(DostapnostOK[i])

    #         #KONVERZIJA OD LISTA VO STRING
    #         opis=OpisOK[i]
    #         opis2=''
    #         mesto=' ' #PROBAAJ SO TAB ili NESTO DRUGO ZA DA SE RAZDVOJAT VIZUELNO/EXCEL ======================== POVTORI GO ISTOTO ZA OPIS
    #         opis2=mesto.join(OpisOK[i])

    #         #informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],ArtiklIME[i],opis2]
    #         #print('OPIS',informacii)
    #         #writer.writerow(informacii)

    #         c=CenaOK[i]
    #         c[0]=c[0].replace(',','')
    #         c[1]=c[1].replace(',','')
    #         c[0]=c[0].replace(' Ден','')
    #         c[1]=c[1].replace(' Ден','')
    #         c[1]=c[1].replace('.','')
    #         informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],ArtiklIME[i],c[0],c[1],POENIOK[i],GarancijaOK[i],links_produkti[i],opis2,salon2]
            
    #         #informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],salon2]
    #         #print(informacii)
    #         writer.writerow(informacii)

    #PISUVA VO FILE INSOMNIA FILE
    with open (filepath6,'w',encoding='utf8',newline='') as f:
         writer= csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
         #header=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Memmory Type','Capacity','GPU','Video Memmory','Screen Size','Refresh Rate','Motherboard','CPU','RAM','SSD','HDD','PSU','CPU Cooler','Case','Bazna Frekvencija','Maksimalna bust frekvencija','Broj na fizicki jadra','Broj na logicki jadra','L3 kes memorija','Arhitektura','TDP','Procesor','RAM memorija','Graficka karticka','Operativen sistem','Garancija','Socket - leziste','Chipset','RAM type','RAM DIMMs','USB 3.1 ports','m.2','SATA','Frekvencija','Interfejt','Kapacitet','Izdrzlivost - TBW','Sifra na artikl','Sifra']
         header=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Garancija','Sifra na artikl','Sifra','BrendID','KategorijaID','Kategorija']

         writer.writerow(header)
         #writer.write('\n')    #_csv.writer' object has no attribute 'write' -------------------------------------

         Category=''
         if NameKat=='Laptopi':
            Category='Лаптопи нетбуци преносни компјутери и опрема/Лаптоп компјутери'
         elif NameKat=='LaptopDopolnitelna':
            Category='Лаптопи нетбуци преносни компјутери и опрема/Додатоци и галантерија за лаптопи'
         elif NameKat=='Graficki':
            Category='Компјутерски компоненти/Графички карти'
         elif NameKat=='HardDisk':
            Category='Компјутерски компоненти/Хард-дискови и SSD'
         elif NameKat=='Procesori':
            Category='Компјутерски компоненти/Десктоп процесори Intel и AMD'
         elif NameKat=='RAM':
            Category='Компјутерски компоненти/RAM мемории'
         elif NameKat=='MaticniPloci':
            Category='Компјутерски компоненти/Матични плочи'
         elif NameKat=='Kuleri':
            Category='Компјутерски компоненти/Ладење'
         elif NameKat=='Kukista':
            Category='Компјутерски компоненти/Куќишта'
         elif NameKat=='Napojuvanja':
            Category='Компјутерски компоненти/Напојувања (PSU)'
         elif NameKat=='Monitori':
            Category='Периферија и галантерија/Монитори'
         elif NameKat=='Tastaturi':
            Category='Периферија и галантерија/Тастатури'
         elif NameKat=='Gluvci':
            Category='Периферија и галантерија/Глувчиња и падови за глувчиња'
         elif NameKat=='WebKameri':
            Category='Периферија и галантерија/Web камери'
         elif NameKat=='Pecatari':
            Category='Office конфигурации и опрема/Office и home принтери скенери и друга опрема'
         elif NameKat=='Skeneri':
            Category='Office конфигурации и опрема/Office и home принтери скенери и друга опрема'
         elif NameKat=='Toneri':
            Category='Office конфигурации и опрема/Office и home принтери скенери и друга опрема'
         elif NameKat=='EksterniDiskovi':
            Category='Периферија и галантерија/Надворешни дискови'
         elif NameKat=='USBMemorii':
            Category='Периферија и галантерија/Мемориски картички и USB мемории'
         elif NameKat=='MemoriskiKarticki':
            Category='Периферија и галантерија/Мемориски картички и USB мемории'
         elif NameKat=='TVZvucni':
            Category='Периферија и галантерија/Слушалки звучници микрофони и аудио опрема'
         elif NameKat=='Slusalki':
            Category='Периферија и галантерија/Слушалки звучници микрофони и аудио опрема'
         elif NameKat=='Konfiguracii':
            Category='Gaming конфигурации и опрема/Gaming Конфигурации'
         elif NameKat=='Mrezna Oprema':
            Category='Периферија и галантерија/Кабли и приклучоци'
         elif NameKat=='KabliKonektori':
            Category='Периферија и галантерија/Кабли и приклучоци'
         elif NameKat=='Multimedia':
            Category='Периферија и галантерија/Кабли и приклучоци'
         elif NameKat=='KompjuterskiDodatoci':
            Category='Периферија и галантерија/Кабли и приклучоци'
         elif NameKat=='OptickiUredi':
            Category='Периферија и галантерија/Останато'
         
         

         elementi=len(SifraOK)
         listaelementi=list(range(0,elementi)) #elementi-1
         #print(listaelementi)
         for i in listaelementi:
             #print(DostapnostOK[i])
             Salon=DostapnostOK[i]
             dolzina=len(DostapnostOK[i])
             if DostapnostOK[i]=='':
                 DostapnostOK[i]='NaN'
             
             GarancijaOK[i]=GarancijaOK[i].replace(': ','')
             #KONVERZIJA OD LISTA VO STRING
             salon=DostapnostOK[i]
             salon2=''
             mesto=' ' #PROBAAJ SO TAB ili NESTO DRUGO ZA DA SE RAZDVOJAT VIZUELNO/EXCEL ======================== POVTORI GO ISTOTO ZA OPIS
             salon2=mesto.join(DostapnostOK[i])


             #KONVERZIJA OD LISTA VO STRING
             opis=OpisOK[i]
             opis2=''
             mesto=' ' #PROBAAJ SO TAB ili NESTO DRUGO ZA DA SE RAZDVOJAT VIZUELNO/EXCEL ======================== POVTORI GO ISTOTO ZA OPIS
             opis2=mesto.join(OpisOK[i])
             #opis2=''
             
             #opis2=mesto.join(OpisOK[i])
             #opis2.replace('\r','')
             #opis2.replace('\n','')
             #print(opis)

             #opis.replace('\r',' ')
             #opis.replace('\n',' ')
             #print('OP111111',opis)
             #opis=opis.split(" ")
             #opis=mesto.join(opis)
             #opis=opis.splitlines()
             #opis=mesto.join(opis)
             #opis=opis.split(',')
             #opis=mesto.join(opis)
             #opis.replace(',',' ')
             #print('OPIIIIIISSS',opis)
             

             #print(opis)
             #print(opis2)
             #informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],ArtiklIME[i],opis2]
             #print('OPIS',informacii)
             #writer.writerow(informacii)
             #c=CenaOK[i]
             #c=c.replace('/n','')
             #c=c.replace(' ','')
             #c=c.replace('|','')
             #c=int(c)
             #c=str(c)
             #print(CenaOK[i])
             c=CenaOK[i]
             c[0]=c[0].replace(',','')
             c[1]=c[1].replace(',','')
             c[0]=c[0].replace(' Ден','')
             c[1]=c[1].replace(' Ден','')
             c[1]=c[1].replace('.','') #KLUB CENA
             if c[1]=='NaN':
                c[1]=c[0]
            #  c[0]=c[0].replace(',','')
            #  c[1]=c[1].replace(',','')
            #  c[0]=c[0].replace(' Ден','')
            #  c[1]=c[1].replace(' Ден','')
            #  c[1]=c[1].replace('.','')
             
             linkkk=ArtiklIME[i]
             linkkk=linkkk.replace(' ','-')

             opishtml=OpisHtmlOK[i]
             Mkeywords=''
             Mkeywords=ArtiklIME[i]+' '+Brend[i]+' '+Category
             
             c[1]=float(c[1])
             c[1]=c[1]*0.98
             c[1]=round(c[1],-1)-1

             if Brend[i]=='':
                Brend[i]='XXX'

             SifraOK[i].strip()
             if SifraOK[i].isnumeric():
                print()
             else:
                SifraOK[i]='00000'
             
             BrendID=0
             if Brend[i]=='A-DATA':
                BrendID=1
             elif Brend[i]=='Acer':
                BrendID=2
             elif Brend[i]=='AFOX':
                BrendID=3
             elif Brend[i]=='AMD':
                BrendID=4
             elif Brend[i]=='AOC':
                BrendID=5
             elif Brend[i]=='Apple':
                BrendID=6
             elif Brend[i]=='Asrock':
                BrendID=7
             elif Brend[i]=='Asus':
                BrendID=8
             elif Brend[i]=='Belkin':
                BrendID=9
             elif Brend[i]=='Brother':
                BrendID=10
             elif Brend[i]=='Canon':
                BrendID=11
             elif Brend[i]=='Choiix':
                BrendID=12
             elif Brend[i]=='Cirkuit Planet':
                BrendID=13
             elif Brend[i]=='Cooler Master':
                BrendID=14
             elif Brend[i]=='Corsair':
                BrendID=15
             elif Brend[i]=='Crucial':
                BrendID=16
             elif Brend[i]=='DeepCool':
                BrendID=17
             elif Brend[i]=='DELL':
                BrendID=18
             elif Brend[i]=='Delux':
                BrendID=19
             elif Brend[i]=='DICALLO':
                BrendID=20
             elif Brend[i]=='DORR':
                BrendID=21
             elif Brend[i]=='EVGA':
                BrendID=22
             elif Brend[i]=='Fortron':
                BrendID=23
             elif Brend[i]=='Genius':
                BrendID=24
             elif Brend[i]=='Gigabyte':
                BrendID=25
             elif Brend[i]=='Grundig':
                BrendID=26
             elif Brend[i]=='HAMA':
                BrendID=27
             elif Brend[i]=='HP':
                BrendID=28
             elif Brend[i]=='Huawei':
                BrendID=29
             elif Brend[i]=='HYNIX':
                BrendID=30
             elif Brend[i]=='HyperX':
                BrendID=31
             elif Brend[i]=='Intel':
                BrendID=32
             elif Brend[i]=='J&A':
                BrendID=33
             elif Brend[i]=='Kingston':
                BrendID=34
             elif Brend[i]=='Labtec':
                BrendID=35
             elif Brend[i]=='LC-Power':
                BrendID=36
             elif Brend[i]=='Lenovo':
                BrendID=37
             elif Brend[i]=='LG':
                BrendID=38
             elif Brend[i]=='Logic':
                BrendID=39
             elif Brend[i]=='Logitech':
                BrendID=40
             elif Brend[i]=='Maxtor':
                BrendID=41
             elif Brend[i]=='Microsoft':
                BrendID=42
             elif Brend[i]=='Midland':
                BrendID=43
             elif Brend[i]=='Modecom':
                BrendID=44
             elif Brend[i]=='MSI':
                BrendID=45
             elif Brend[i]=='Olympia':
                BrendID=46
             elif Brend[i]=='Panasonic':
                BrendID=47
             elif Brend[i]=='Philips':
                BrendID=48
             elif Brend[i]=='Pioneer':
                BrendID=49
             elif Brend[i]=='Power Box':
                BrendID=50
             elif Brend[i]=='PQI':
                BrendID=51
             elif Brend[i]=='Razer':
                BrendID=52
             elif Brend[i]=='Roadstar':
                BrendID=53
             elif Brend[i]=='Roline':
                BrendID=54
             elif Brend[i]=='Samsung':
                BrendID=55
             elif Brend[i]=='Sapphire':
                BrendID=56
             elif Brend[i]=='Seagate':
                BrendID=57
             elif Brend[i]=='SONY':
                BrendID=58
             elif Brend[i]=='Spire':
                BrendID=59
             elif Brend[i]=='ST':
                BrendID=60
             elif Brend[i]=='TeamGroup':
                BrendID=61
             elif Brend[i]=='Thomson':
                BrendID=62
             elif Brend[i]=='Toshiba':
                BrendID=63
             elif Brend[i]=='TP-Link':
                BrendID=64
             elif Brend[i]=='Various':
                BrendID=65
             elif Brend[i]=='WesternDigital':
                BrendID=66
             elif Brend[i]=='X5TECH':
                BrendID=67
             elif Brend[i]=='XFX':
                BrendID=68
             elif Brend[i]=='Xiaomi':
                BrendID=69
             elif Brend[i]=='XXX':
                BrendID=70



             #47344_0-1000x1000.jpg
             imeslika=''
             imeslika=SifraOK[i]+'_0-1000x1000.jpg'


             #header=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Memmory Type','Capacity','GPU','Video Memmory','Screen Size','Refresh Rate','Motherboard','CPU','RAM','SSD','HDD','PSU','CPU Cooler','Case','Базна фрекфенција','Максимална буст фреквенција','Број на физички јадра','Број на логички јадра','L3 кеш меморија','Архитектура','TDP','Процесор','RAM меморија','Графичка картичка','Оперативен систем','Гаранција','Socket - лежиште','Chipset','RAM type','RAM DIMMs','USB 3.1 ports','m.2','SATA','Фреквенција','Интерфејс','Капацитет','Издржливост - TBW','Шифра на артикл','Шифра']
             header=['Category','Brand','Product','Variant','SKU','Price','Old Price','Currency','Weight','Stock','Units','Visible','Featured','Meta title','Meta keywords','Meta description','Annotation','Description','Images','URL','Гаранција','Шифра на артикл','Шифра']

             #informacii=[RedenBrojIDOK[i],NameKat,BrendOK[i],SifraOK[i],ArtiklIME[i],c,'0',POENIOK[i],GarancijaOK[i],links_produkti[i],opis,salon2,'Компјутерски делови']
             #informacii=[Category,Brend[i],ArtiklIME[i],'','',c[1],c[0],'1',POENIOK[i],'1','0','1','0',ArtiklIME[i],Mkeywords,opis2,'',opishtml,imeslika,linkkk,"""memory""",'capacity','GPU','video','screen size','refresh','motherborad','cpu','ram','ssd','hdd','psu','cpucooler','case','bazna','maks','broj fizicki','broj logicki','l3','arhitektura','tdp','procesor','ram','graficka','operativen',GarancijaOK[i],'socket','chipset','tipram','ramdimm','usb','m2','sata','frekvencija','interface','kapacitet','izdrzlivost','SA_'+SifraOK[i],SifraOK[i]]
             informacii=[Category,Brend[i],ArtiklIME[i],'','SE_'+SifraOK[i],c[1],'0','1','',POENIOK[i],'0','1','0','','',opis2,'',opishtml,imeslika,linkkk,GarancijaOK[i],'SE_'+SifraOK[i],'SE_'+SifraOK[i],BrendID,'kategorijaID',NameKat]
             #informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],salon2]
             #print(informacii)
             writer.writerow(informacii)
             #informacii=[RedenBrojIDOK[i],NameKat,SifraOK[i],ArtiklIME[i],c[0],c[1],POENIOK[i],GarancijaOK[i],links_produkti[i],opis2,salon2]




#DOPOLNI LISTA SO KATEGORII OD EXCEL





#Laptopi
#https://setec.mk/index.php?route=product/category&path=10002_10003/en&limit=100
#Laptopi Dopolnitelna
#https://setec.mk/index.php?route=product/category&path=10002_10005&limit=100
#Monitori
#https://setec.mk/index.php?route=product/category&path=10019_10031
#Konfiguracii
#https://setec.mk/index.php?route=product/category&path=10019_10032
#Kukista
#https://setec.mk/index.php?route=product/category&path=10019_10020_10028
#Kuleri
#https://setec.mk/index.php?route=product/category&path=10019_10020_10027
#Graficki karti
#https://setec.mk/index.php?route=product/category&path=10019_10020_10025
#Hard Disk
#https://setec.mk/index.php?route=product/category&path=10019_10020_10023
#Maticni Ploci
#https://setec.mk/index.php?route=product/category&path=10019_10020_10022
#Opticki Uredi
#https://setec.mk/index.php?route=product/category&path=10019_10020_10026
#Napojuvanja
#https://setec.mk/index.php?route=product/category&path=10019_10020_10029
#Procesori
#https://setec.mk/index.php?route=product/category&path=10019_10020_10021
#RAM Memorii
#https://setec.mk/index.php?route=product/category&path=10019_10020_10024
#TV Zvucni Karti
#https://setec.mk/index.php?route=product/category&path=10019_10020_10030
#Tastaruri
#https://setec.mk/index.php?route=product/category&path=10019_10038_10040
#Gluvci
#https://setec.mk/index.php?route=product/category&path=10019_10038_10039
#Prenosni Kutii
#https://setec.mk/index.php?route=product/category&path=10019_10038_10042
#Web Kameri
#https://setec.mk/index.php?route=product/category&path=10019_10038_10041
#Pecatari
#https://setec.mk/index.php?route=product/category&path=10019_10033
#Skeneri
#https://setec.mk/index.php?route=product/category&path=10019_10035
#Toneri
#https://setec.mk/index.php?route=product/category&path=10019_10036
#Mrezna Oprema
#https://setec.mk/index.php?route=product/category&path=10019_10037
#Slusalki
#https://setec.mk/index.php?route=product/category&path=10019_10043
#USB memorii
#https://setec.mk/index.php?route=product/category&path=10019_10044
#Memoriski karticki
#https://setec.mk/index.php?route=product/category&path=10019_10045
#Softver
#https://setec.mk/index.php?route=product/category&path=10019_10046
#Eksterni Diskovi
#https://setec.mk/index.php?route=product/category&path=10019_10047
#Kabli i konektori
#https://setec.mk/index.php?route=product/category&path=10019_10051
#Multimedia
#https://setec.mk/index.php?route=product/category&path=10019_10053
#Kompjuterski Dodatoci
#https://setec.mk/index.php?route=product/category&path=10019_10223 ASsa

