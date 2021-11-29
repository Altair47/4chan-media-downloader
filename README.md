# 4chan-media-downloader
Python script to download all media from any thread in 4chan, with options to download to specific folder, make subfolders for each thread or board and autoscrap per specified minutes.

Dependencies: requests,bs4
Usage: 4chan.py [-h] (-t THREAD | -l LIST) [-f USERFOLDER] [-m MINUTES] [-b BATCH]
options:
  -h, --help
  -t THREAD, --thread Thread link
  -l LIST, --list LIST  Path to list.
  -f USERFOLDER, --folder USERFOLDER
        Specify in which folder to save the thread or the link of threads and their subfolders. If folder doesnt exist or isnt specified, creates one with thread name.
  -m MINUTES, --minutes MINUTES
        Autorun every -m or --minutes. OFF if not specified
  -b BATCH, --batch BATCH
        Batch download without making subfolder for threads
Example: 
python 4chan.py -l 4links.txt -f .
      Will download all media from each link on 4links.txt on the folder you run it from with subfolders for each link.
python 4chan.py -t https://boards.4channel.org/vrpg/thread/2
      Will make a folder called 4chan on the spicific directory and its gonna create another folder inside with thread name and then download all media from thread.