# 4chan-media-downloader
Python script to download all media from any thread in 4chan, with options to download to specific folder, make subfolders for each thread, batch download, ASCI art of thumbnail on terminal, chose only specific extension, autoscrap per specified minutes.

Dependencies: **requests, bs4, climage(required only for -i argument)** \
Usage:  4chan.py [-h] (-t THREAD || -l LIST) [-f USERFOLDER] [-m MINUTES] [-b BATCH] [-i IMAGE] \
Requires at least Thread(-t) or List(-l) argument, all else are optional.

    -h, --help
    
    -t , --thread : {THREAD}
    Thread link.
    
    -l, --list : {LIST}
    Path to list file.
  
    -f, --folder : {USERFOLDER}
    Specify in which folder to save the thread or the list of threads and their subfolders. 
    If folder doesnt exist or isnt specified, creates one with thread name.

    -m, --minutes : {MINUTES}
    Autorun every -m or --minutes. OFF if not specified.
  
    -b, --batch 
    If enabled Batch download without making subfolder for threads.

    -e, --extension : {EXTENSION}
    Specify the extension of the files to download.

    -i, --image
    If enabled, display an image preview like the one on the video bellow (requires climage)

[![asciicast](https://asciinema.org/a/7X66gWWSMufdCgkLVdT9100qi.svg)](https://asciinema.org/a/7X66gWWSMufdCgkLVdT9100qi)

**Examples:**

    python 4chan.py -t https://boards.4channel.org/vrpg/thread/2
Will make a folder on the current directory with thread name and then download all media from thread.

    python 4chan.py -l 4links.txt -f .
Will create a subfolder with the name and board of each thread/link in **4links.txt** and download every media on it.