#!/usr/bin/env python
# coding: utf-8

import requests
import time
from bs4 import BeautifulSoup
import re
import os

forb=('<>:"/\|?*')
fpage=input("Input thread to start downloading all media: ")
url=fpage
r = requests.get(url)
names=list()
links=list()
soup = BeautifulSoup(requests.get(url).text, 'lxml')
containers = soup.findAll("div", {"class": "fileText"})
left='href="//'
right='" target'

#Folder name
dirname = soup.find("title").text
print(dirname)
dirname=dirname[dirname.find('-')+2:dirname.rfind('-')-1]
for char in forb:
    dirname = dirname.replace(char,'!')
if not os.path.exists(dirname):
    os.makedirs(dirname)
os.chdir(dirname)

for index,c in enumerate(containers):
    s = (str(c))
    n = (str(c.text))
    links.append(s[s.index(left)+len(left):s.index(right)])
    names.append(c.find('a', href=True).text)
    print ('HTML:',s,'\nLINK: ',s[s.index(left)+len(left):s.index(right)],'\nFull',c.text,'\nCLEAN NAME:', (n[n.index('File: ')+len('File: '):n.index(' (')]),'\nINDEX: ',index,'\nPercentage Completed:',round((index+1)*100/len(containers)),'\n')
    k = requests.get('http://'+links[-1], allow_redirects=True)
    open(names[-1], 'wb').write(k.content)
    
    #Rule of three for percentage
