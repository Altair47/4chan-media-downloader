#!/usr/bin/env python
# coding: utf-8

import requests, time, os, sys, re, argparse
from bs4 import BeautifulSoup

forb=('<>:"/\|?*')
left='href="//'
right='" target'
#Page
#url=input("Input thread to start downloading all media: ")

def mkdir(dirname):
    for char in forb:
        dirname = dirname.replace(char,'!')
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    os.chdir(dirname)

def Scrap(url):
    r = requests.get(url)
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    try:
        #If thread is dead, attempt to delete the line from the 4links.txt
        if soup.h2.text=='404 Not Found':
            print('Thread is dead!')
            try:
                with open('4links.txt', 'r') as fr:
                    lines = fr.readlines()
                    with open('4links.txt', 'w') as fw:
                        for line in lines:
                            # strip() is used to remove '\n'
                            # present at the end of each line
                            if line.strip('\n') != url:
                                fw.write(line)
                print("Deleted from the file!")
            except:
                print("Oops! something error")
            return
    except:
        print('Thread exists.')
    containers = soup.findAll("div", {"class": "fileText"})
    #Make directory
    dirname = soup.find("title").text
    print(dirname,'\n')
    dirname=dirname[dirname.find('-')+2:dirname.rfind('-')-1]
    mkdir(dirname)
    #Loop media download
    for index,c in enumerate(containers):
        s = (str(c))      #s=whole eg[<div class="fileText" id="fT3962922">File: <a href="//i.4cdn.org/wsg/1622452136055.webm" target="_blank">Some stuff never changes.webm</a> (3.85 MB, 336x190)</div>]
        n = (str(c.text)) #n=name  eg[File: Some stuff never changes.webm (3.85 MB, 336x190)]
        link = s[s.index(left)+len(left):s.index(right)] #[i.4cdn.org/wsg/1622224877680.webm]
        name = c.find('a', href=True).text               #[let it sneed.webm]
        name = ' '.join((name[:name.rfind('.')],link[link.rfind('/')+1:])) #[let it sneed 1622224877680.webm]
        #Calculating size if required
        #   linksize = int((urllib.request.urlopen('https://'+link)).info()['Content-Length'])
        #   filesize= int(os.stat(name).st_size)
        #   if os.path.exists(name) and filesize==linksize:
        if os.path.exists(name):
            #print("File'",name,"'already exists, with size:",os.stat(name).st_size)
            continue
        else:
            k = requests.get('http://'+link, allow_redirects=True)
            for char in forb:
                name = name.replace(char,'!')
            open(name, 'wb').write(k.content)
            print ('HTML:',s,'\nLINK: ',s[s.index(left)+len(left):s.index(right)],'\nFull',c.text,'\nCLEAN NAME:', (n[n.index('File: ')+len('File: '):n.index(' (')]),'\nINDEX:',index,'\nSaved as:',name,'\nPercentage Completed:',round((index+1)*100/len(containers)),'\nFrom:',dirname,'\n') #rule of three for percentage
    os.chdir('..')


while 1:
    file1 = open('4links.txt', 'r')
    Lines = file1.readlines()
    file1.close()
    Lines = [x.strip() for x in Lines]
    for url in Lines:
        Scrap(url)
        time.sleep(1)
    for i in reversed(range(1,21)):#repeat every 20 minutes
        print(i,'minutes until next scrap')
        time.sleep(60)