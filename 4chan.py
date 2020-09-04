#!/usr/bin/env python
# coding: utf-8

# In[23]:


import requests
import time
from bs4 import BeautifulSoup
import re
import os


# In[85]:

fpage=input("Input thread to start downloading all media: ")
url=fpage
r = requests.get(url)
#print(r.text)
#print(r.headers.get('content-type'))
names=list()
links=list()
soup = BeautifulSoup(requests.get(url).text, 'lxml')
containers = soup.findAll("div", {"class": "fileText"})
left='href="//'
right='" target'
'''
for s in containers:
    strcon.append(str(s))
for s in strcon:
    print (s)
    print (s[s.index(left)+len(left):s.index(right)],'\n')
    links.append(s[s.index(left)+len(left):s.index(right)])'''
for index,c in enumerate(containers):
    s = (str(c))
    n = (str(c.text))
    #for a in c.find_all('a', href=True):
    #    print ("Found the Name:", a.text)
    links.append(s[s.index(left)+len(left):s.index(right)])
    #names.append(n[n.index('File: ')+len('File: '):n.index(' (')])
    names.append(c.find('a', href=True).text)
    print ('HTML:',s,'\nLINK: ',s[s.index(left)+len(left):s.index(right)],'\nFull',c.text,'\nCLEAN NAME: ', (n[n.index('File: ')+len('File: '):n.index(' (')]),'\nINDEX: ',index,'\nPercentage Completed:',round((index+1)*100/len(containers)),'\n')
    k = requests.get('http://'+links[-1], allow_redirects=True)
    open(names[-1], 'wb').write(k.content)
    
    #rule of three for percentage


    


# In[25]:


'''for link in links:
    r = requests.get(link, allow_redirects=True)
    open(name, 'wb').write(r.content)
    '''


# In[ ]:


'''url='https://i.4cdn.org/wsg/1596086200370.webm'
sep=url.rindex('/')
name=url.rsplit('/',1)[1]
r = requests.get(url, allow_redirects=True)
open(name, 'wb').write(r.content)
#re.sub(/^(.*[\\\/])/'', '', url)ss'''

