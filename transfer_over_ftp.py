from ftplib import FTP
import os
import time

host = 'xxx.xxx.xxx.159'
port = 3721


ftp = FTP(timeout=5)
ftp.connect(host, port)
ftp.login('anonymous', '')
#set ftp working folder
"The folder path of remote ftp machine"
"Also we will monitor this folder using Tasker, which will trigger TTS action as folder gets modified"
ftp.cwd("/storage/emulated/0/Download/sm")
"local path to the tweets.html that we generated in twitter_scrape.py"
fp = open("tweets.html", 'rb')
ftp.storbinary('STOR %s' % os.path.basename("tweets.html"), fp, 1024)
fp.close()
print('done')
