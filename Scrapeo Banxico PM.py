# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 01:22:10 2022

@author: jujo_

Scrapeo de anuncios de politica monetaria de Banxico
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import glob 
import errno

# Working directory
os.chdir('D:/Escritorio/Scrapeo Banxico PM')

## Creamos la carpeta (en caso que no exista) donde alojaremos los archivos

try:
    os.mkdir('in')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

## Limpiamos todo su contenido que pudiera tener para evitar duplicados

files = glob.glob('in/*.pdf') 
for f in files: 
    os.remove(f)

## Pagina a examinar
URL = "https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html"
URL_req = requests.get(URL)
URL_soup = BeautifulSoup(URL_req .text, 'html.parser')

urls = []
for link in URL_soup.find_all('a'):
    urls.append(link.get('href'))

df = pd.DataFrame(urls,columns =['URLS'])

# Nos quedamos unicamente con los anuncios de politica monetaria
df = df[df['URLS'].str.contains("/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/")]

df['URLS'] = "https://www.banxico.org.mx" + df['URLS']

## Extraemos la tabla que sistematiza los anuncios
URL_web = pd.read_html(URL) 

URL_web_table = URL_web[0]
URL_web_table.iloc[:,0] = URL_web_table.iloc[:,0].str.replace('/','-')

###############################################################################

# Descargar pdf's
for enlace in range(0,len(URL_web_table.iloc[:,0])):
    print(enlace+1)
    myfile = requests.get(df.iloc[enlace,0])
    open('in/'+str(enlace+1)+'-BANXICO-PM-'+URL_web_table.iloc[enlace,0]+'.pdf', 'wb').write(myfile.content)