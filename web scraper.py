# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 18:29:02 2018

@author: Scurtu Mihai
"""


from urllib.error import HTTPError
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re
import csv
import time
import requests
import os



def anunt(link):
    try:
        html = urlopen(link)
    except HTTPError as e: #in caz ca nu poate deschide anuntul
        print(link)
        return None       
    except requests.ConnectionError as e: #am primit eroare de conectare asa ca am pus sa incerce inca o data dupa 120 de secunde
        time.sleep(120)
        print(link)
        anunt(link)
    anunt= bs(html.read(), 'html.parser')  #deschidem cu beautiful soup link-ul
    try:
        titlu_anunt = anunt.h1.text  #titlul era cu h1
        #titlu_anunt = titlu_anunt
    except AttributeError: #in caz ca nu gaseste dupa codul html sa nu mai incerce
        print(link)
        return None
    
    dictionar={}   
    
    #print(titlu_anunt)
    
    try:
        pret = anunt.find('div', {'id':'detaliu-pret-mob'}).text #pretul era intr-un div cu id-ul respectiv
        pret = pret.replace('\t', '') #am inlocuit tab-urile
        pret = pret.replace('\n', '') #am inlocuit liniile noi ca sa avem textul curatat
    except AttributeError:
        print(link)
        return None
    
    #print(pret)
    
    
    try:
        detalii = anunt.find('div', {'id':'actiuni-mob'}).text
        detalii = detalii.encode('utf-8')
    except AttributeError:
        print(link)
        return None
    
    try:
        oras = anunt.find('div', {'id':'detaliu-localitate'}).text
        oras = oras.replace('\t', '') #am inlocuit tab-urile
        oras = oras.replace('\n', '')
        dictionar['oras']=oras
    except KeyError:
        print(link)
        dictionar['oras']= None
        
    try:
        descriere_text = anunt.find('p', {'class':'descriere-text'}).text
        descriere_text = descriere_text.replace('\t', '') #am inlocuit tab-urile
        descriere_text = descriere_text.replace('\n', '')
        dictionar['descriere']= descriere_text
    except KeyError:
        print(link)
        dictionar['descriere']= None
    #print(detalii)
    
    """am avut 2 coloane, una cu descrierea si una cu valorile"""
    coloana = anunt.find_all('div', {'class':"actiuni-col-a"})
    descriere = anunt.find_all('div', {'class':'actiuni-col-b'})
    lista_coloana=[]
    lista_descriere=[]
    
    for i in coloana:
        cuvant = i.text
        cuvant_bun = cuvant.replace('\t', '')
        cuvant_bun = cuvant_bun.replace('\n', '')
        #cuvant_bun = cuvant_bun.encode('utf-8')
        lista_coloana.append(cuvant_bun)
        #lista_coloana.append(i.text)
    for i in descriere:
        cuvant = i.text
        cuvant_bun = cuvant.replace('\t', '')
        cuvant_bun = cuvant_bun.replace('\n', '')
        #cuvant_bun = cuvant_bun.encode('utf-8')
        lista_descriere.append(cuvant_bun)
        #lista_descriere.append(i.text)
    
    descriere = dict(zip(lista_coloana, lista_descriere)) #am facut un dictionar din descirea valorii si valoare
    
    ''' Am preluat din variabilele si din dictionarul cu descrierea valorile si le-am pus intr-un dictionar final
    In caz ca nu am gasit valori le vom avea ca valori nule si le vom trata separat in Pandas
    '''
    try:
        dictionar['titlu']=titlu_anunt
    except KeyError:
        dictionar['titlu']= None
    try:
        dictionar['pret']=pret
    except KeyError:
        dictionar['pret']= None
    try:
        dictionar['tip_oferta']=descriere['Tip Oferta']
    except KeyError:
        dictionar['tip_oferta']= None
    try:
        dictionar['grad_finisare']=descriere['Grad de finisare']
    except KeyError:
        dictionar['grad_finisare']= None
    try:
        dictionar['persoana']=descriere['Persoana fizica  / Agentie']
    except KeyError:
        dictionar['persoana']= None
    try:
        dictionar['etaj']=descriere['Etaj']
    except KeyError:
        dictionar['etaj']= None
    try:
        dictionar['vechime_imobil']=descriere['Vechime imobil']
    except KeyError:
        dictionar['vechime_imobil']= None
    try:
        dictionar['numar_bai']=descriere['Nr. bai']
    except KeyError:
        dictionar['numar_bai']= None
    try:
        dictionar['numar_balcoane']=descriere['Nr. balcoane']
    except KeyError:
        dictionar['numar_balcoane']= None
    try:
        dictionar['geamuri_termopan']=descriere['Geamuri termopan']
    except KeyError:
        dictionar['geamuri_termopan']= None
    try:
        dictionar['centrala_termica']=descriere['Centrala Termica']
    except KeyError:
        dictionar['centrala_termica']= None
    try:
        dictionar['compatimentare']=descriere['Compartim.']
    except KeyError:
        dictionar['compatimentare']= None
    try:
        dictionar['parchet']=descriere['Parchet']
    except KeyError:
        dictionar['parchet']= None
    try:
        dictionar['confort']=descriere['Confort']
    except KeyError:
        dictionar['confort']= None
    try:
        dictionar['gresie']=descriere['Gresie']
    except KeyError:
        dictionar['gresie']= None
    try:
        dictionar['faianta']=descriere['Faianta']
    except KeyError:
        dictionar['faianta']= None
    try:
        dictionar['zugravit_lavabil']=descriere['Zugravit lavabil']
    except KeyError:
        dictionar['zugravit_lavabil']= None
    try:
        dictionar['loc_parcare']=descriere['Loc parcare']
    except KeyError:
        dictionar['loc_parcare']= None
    try:
        dictionar['agentie']=descriere['Agentie']
    except KeyError:
        dictionar['agentie']= None
    try:
        dictionar['numar_camere']=descriere['Nr. camere']
    except KeyError:
        dictionar['numar_camere']= None
    try:
        dictionar['strada']=descriere['Strada']
    except KeyError:
        dictionar['strada']= None
    try:
        dictionar['suprafata']=descriere['Suprafata']
    except KeyError:
        dictionar['suprafata']= None
    try:
        dictionar['cartier']=descriere['Cartier']
    except KeyError:
        dictionar['cartier']= None
    try:
        dictionar['link']=link
    except KeyError:
        dictionar['link']= None
        
    try:
        dictionar['modificari_interioare']=descriere['Modificari interioare']
    except KeyError:
        dictionar['modificari_interioare']= None
        
    
    try:
        dictionar['balcoane_inchise']=descriere['Balcoane inchise']
    except KeyError:
        dictionar['balcoane_inchise']= None
        
    
    try:
        dictionar['aer_conditionat']=descriere['Aer Conditionat']
    except KeyError:
        dictionar['aer_conditionat']= None
        
    try:
        dictionar['loc_in_pod']=descriere['Loc in pod']
    except KeyError:
        dictionar['loc_in_pod']= None
        
    try:
        dictionar['loc_in_pivnita']=descriere['Loc in pivnita']
    except KeyError:
        dictionar['loc_in_pivnita']= None
        
    try:
        dictionar['uscator']=descriere['Uscator']
    except KeyError:
        dictionar['uscator']= None
            
    #dictionar = {k: unicode(v).encode("utf-8") for k,v in dictionar.iteritems()}
    return dictionar


def linkuri(pagina):
    html = urlopen(pagina)
    anunt= bs(html.read(), 'html.parser')
    '''
    Cu aceasta functie preluam de pe o pagina toate link-urile cu anunturi
    '''
    try:
        link = anunt.find('div',{'id':'mainwrapper'}).find_all('a', {'class':'link_totanunt'})
    except AttributeError:
        print('nenene')
        return None
    #print(link)
    
    lista_linkuri = []
    
    for i in link:
        lista_linkuri.append(i['href'])
        
    return lista_linkuri

def nextpage(prima_pagina):
    html = urlopen(prima_pagina)
    pagina= bs(html.read(), 'html.parser')
    next = pagina.find('a', {'class':"next_page"}) # butonul de next page
    if next is None:
        return None
    ''' aceasta functie ne da link-ul de la urmatoarea pagina '''
    next_page = next['href']
    
    if next_page is None:
        return None
    return next_page



def extragere_pagini(page, csv_pagini):
    list_pag = []
    #page = prima_pagina
    while(page): #cu acest while preluam intr-o lista toate paginile
        #print(page)
        list_pag.append(page)
        page = nextpage(page)
        
    print(list_pag)
    
    out = csv.writer(open(csv_pagini,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    out.writerow(list_pag)
    
    

def extragere_anunturi(csv_pagini, csv_anunturi):
    lista_pagini = []
    lista_anunturi = []
    #lista= []
    with open(csv_pagini, newline='') as csvfile:
        pagini = csv.reader(csvfile)
        #print(type(pagini))
        lista = list(pagini)
        print(type(lista))
        print(lista)
        for i in lista[0]:
            lista_pagini.append(i)
        #cu aceasta functie citim fisierul csv care contine paginile si le vom pune intr-o lista
        #print(lista_pagini)
        print(len(lista_pagini)) #vedem cate pagini avem
        for i in lista_pagini:
            anunturi = linkuri(i)
            for x in anunturi:
                lista_anunturi.append(x)
    out = csv.writer(open(csv_anunturi,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    out.writerow(lista_anunturi)
    print(lista_anunturi)

def extragere_info(csv_anunturi, csv_info):
    lista_anunturi = []
    print("ANUNTURI FINALE!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #print(lista_anunturi)
    
    with open(csv_anunturi, newline='') as csvfile:
        anunturi = csv.reader(csvfile)
        #print(type(anunturi))
        lista = list(anunturi)
        #print(lista)
        #print(type(lista))
        for i in lista[0]:
            lista_anunturi.append(i)
    print(len(lista_anunturi))
    print(lista_anunturi)
    
    with open(csv_info, 'w', encoding='utf-8') as f:
        coloane=['titlu', 'pret', 'oras', 'grad_finisare', 'descriere', 'tip_oferta', 'persoana', 'etaj', 'vechime_imobil', 'numar_bai', 'numar_balcoane', 'geamuri_termopan', 'centrala_termica', 'compatimentare', 'parchet', 'confort', 'gresie', 'faianta', 'zugravit_lavabil', 'loc_parcare', 'agentie', 'numar_camere', 'strada', 'suprafata', 'cartier', 'link', 'modificari_interioare', 'balcoane_inchise', 'aer_conditionat', 'loc_in_pod', 'loc_in_pivnita', 'uscator']
        csv_writer= csv.DictWriter(f, fieldnames=coloane, delimiter='\t')
        csv_writer.writeheader()
        for y in lista_anunturi:
            dictionar = anunt(y)
            if dictionar is None:
                csv_writer.writerow({'titlu': 'Nu a fost deschis anuntul'})
            else:
                try:
                    csv_writer.writerow({'titlu':dictionar['titlu'], 'grad_finisare':dictionar['grad_finisare'],'pret':dictionar['pret'], 'oras':dictionar['oras'], 'descriere':dictionar['descriere'], 'tip_oferta':dictionar['tip_oferta'], 'persoana':dictionar['persoana'], 'etaj':dictionar['etaj'], 'vechime_imobil':dictionar['vechime_imobil'], 'numar_bai':dictionar['numar_bai'], 'numar_balcoane':dictionar['numar_balcoane'], 'geamuri_termopan':dictionar['geamuri_termopan'], 'centrala_termica':dictionar['centrala_termica'], 'compatimentare':dictionar['compatimentare'],  'parchet':dictionar['parchet'], 'confort':dictionar['confort'], 'gresie':dictionar['gresie'], 'faianta':dictionar['faianta'], 'zugravit_lavabil':dictionar['zugravit_lavabil'], 'loc_parcare':dictionar['loc_parcare'], 'agentie':dictionar['agentie'], 'numar_camere':dictionar['numar_camere'], 'strada':dictionar['strada'], 'suprafata':dictionar['suprafata'], 'cartier':dictionar['cartier'], 'link':dictionar['link'], 'modificari_interioare':dictionar['modificari_interioare'], 'balcoane_inchise':dictionar['balcoane_inchise'], 'aer_conditionat':dictionar['aer_conditionat'], 'loc_in_pod':dictionar['loc_in_pod'],  'loc_in_pivnita':dictionar['loc_in_pivnita'], 'uscator':dictionar['uscator']})
                except KeyError as e:
                    print("KeyError: {0}".format(e))
    print('GATA!!!!!')
   
#asta = nextpage('http://www.piata-az.ro/anunturi/garsoniere-de-vanzare-1000?f_valuta=+70525&country=1&f_region=+1001&f_city=+2001&f_tip_oferta=+70406')
#print(asta)
    

    
fisier_pagini = 'listanouapagini.csv'
fisier_adrese = 'listanouaadreseanunturi.csv'
fisier_final = 'anunturinouagarsoniere1.csv'

_ = extragere_pagini('http://www.piata-az.ro/anunturi/garsoniere-de-vanzare-1000?f_valuta=+70525&country=1&f_region=+1001&f_city=+2001&f_tip_oferta=+70406', fisier_pagini)

__ = extragere_anunturi(fisier_pagini, fisier_adrese)

___ = extragere_info(fisier_adrese, fisier_final)


