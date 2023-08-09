#!/usr/bin/env python
# coding: utf-8

import requests, time, os, sys, re, argparse
from bs4 import BeautifulSoup
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-t", "--thread", help="Link to thread. REQUIRED.")
group.add_argument("-l", "--list", help="Path to list. REQUIRED.")
parser.add_argument("-f", "--folder",dest="userfolder", help="Specify in which folder to save the thread. If folder doesnt exist or not specified creates one with thread name.")
parser.add_argument("-m", "--minutes", help="Autorun every -m or --minutes. OFF if not specified.")
parser.add_argument("-b", "--batch", help="Batch download without making subfolder for threads.",action='store_true')
parser.add_argument("-e", "--extension", help="Download only files with the specific extension.")
parser.add_argument("-i", "--image", help="Image preview while downloading.",action='store_true')
parser.add_argument("-p", "--parallel", help="Split each download into a thread for pallel downloads.",action='store_true')
parser.add_argument("-n", "--nonverbose", help="Shows info for each file downloaded [True,False]. (Disables --image if True)", action='store_true')
args = parser.parse_args()
forb=('<>:"/\|?*')
left='href="//'
right='" target'
#Page
#url=input("Input thread to start downloading all media: ")
if args.parallel:
        import threading

def ImageToTerminal(fName):
    if args.image:
        cmd = ["ffmpeg", "-i", fName, "-vframes", "1", "-f", "image2pipe", "-c:v", "mjpeg", "-", "-hide_banner", "-loglevel", "error"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()
        output = climage.convert(BytesIO(stdout), is_unicode=True, is_256color=1, width=50)
        print(output)
        print(BytesIO(stdout))

def RemoveForbiddenChars(textToReplace):
    for char in forb:
        textToReplace = textToReplace.replace(char,'!')
    return textToReplace

def mkdir(dirname):
    dirname = RemoveForbiddenChars(dirname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    os.chdir(dirname)

def ScrapSite(index,container,dirname,containers,lock):
    containerString = (str(container))      #s=whole eg[<div class="fileText" id="fT3962922">File: <a href="//i.4cdn.org/wsg/1622452136055.webm" target="_blank">Some stuff never changes.webm</a> (3.85 MB, 336x190)</div>]
    nameOnDownload = (str(container.text)) #n=name  eg[File: Some stuff never changes.webm (3.85 MB, 336x190)]
    cleanName = (nameOnDownload[nameOnDownload.index('File: ')+len('File: '):nameOnDownload.index(' (')])
    link = containerString[containerString.index(left)+len(left):containerString.index(right)] #[i.4cdn.org/wsg/1622224877680.webm]
    if args.extension:
        if not link[link.rfind(".")+1:] == args.extension:
            return
    nameOfFile = container.find('a', href=True).text    #[let it sneed.webm]
    nameOfFile = ' '.join((nameOfFile[:nameOfFile.rfind('.')],link[link.rfind('/')+1:])) #[let it sneed 1622224877680.webm]
    #Calculating size if required
    #   linksize = int((urllib.request.urlopen('https://'+link)).info()['Content-Length'])
    #   filesize= int(os.stat(name).st_size)
    #   if os.path.exists(name) and filesize==linksize:
    nameOfFile = RemoveForbiddenChars(nameOfFile)
    if os.path.exists(nameOfFile):
        #print("File'",name,"'already exists, with size:",os.stat(name).st_size)
        return
    else:
        mediaContent = requests.get('http://'+link, allow_redirects=True)
        with open(oldpath+"/"+dirname+"/"+nameOfFile, 'wb') as media:
            media.write(mediaContent.content)
        if not args.nonverbose:
            if args.parallel:
                with lock:
                    #print('HTML:',containerString)
                    print('LINK: ',link)
                    print('Full',container.text)
                    print('CLEAN NAME:',cleanName)
                    print('INDEX:',index)
                    print('Saved as:',nameOfFile)
                    print('Percentage Completed:',round((index+1)*100/len(containers)))
                    print('From:',dirname,'\n')
                    ImageToTerminal(oldpath+"/"+dirname+"/"+nameOfFile)
            else:
                #print('HTML:',containerString)
                print('LINK: ',link)
                print('Full',container.text)
                print('CLEAN NAME:', cleanName)
                print('INDEX:',index)
                print('Saved as:',nameOfFile)
                print('Percentage Completed:',round((index+1)*100/len(containers)))
                print('From:',dirname,'\n')
                ImageToTerminal(oldpath+"/"+dirname+"/"+nameOfFile)

def Scrap(url):
    r = requests.get(url)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
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
                print("Oops! something's wrong")
            return
    except:
        print('Thread exists.')
    containers = soup.findAll("div", {"class": "fileText"})
    #Make directory
    dirname = soup.find("title").text
    print(dirname,'\n')
    dirname=dirname[dirname.find('-')+2:dirname.rfind('-')-1]
    if not args.batch:
        mkdir(dirname)
    dirname = RemoveForbiddenChars(dirname)
    #Loop media download
    if args.parallel:
        lock = threading.Lock()
        threads = list()
        for index,container in enumerate(containers):
            job = threading.Thread(target=ScrapSite, args=(index,container,dirname,containers,lock))
            threads.append(job)
            job.start()
        for index, thread in enumerate(threads): thread.join()
    else:
        for index,container in enumerate(containers):
            ScrapSite(index,container,dirname,containers,0)
    os.chdir('..')

if __name__ == '__main__':
    oldpath = os.getcwd()
    if args.userfolder:
        if not os.path.exists(args.userfolder):
            mkdir(args.userfolder)
    while True:
        if args.image:
            import subprocess
            from io import BytesIO
            import climage
        if args.list:
            with open(args.list, 'r') as file1:
                Lines = file1.readlines()
            Lines = [x.strip() for x in Lines]
            for url in Lines:
                Scrap(url)
        if args.thread:
            Scrap(args.thread)
        if args.minutes:
            print('Sleepign for', args.minutes, 'minutes')
            time.sleep(int(args.minutes)*60)
        if not args.minutes:
            break
    os.chdir(oldpath)
    print('Done!')