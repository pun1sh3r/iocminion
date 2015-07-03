# iocminion
=======
Just another tool to extract IOC's from files. this tool has the capability to extract IOC's from the following sources: pdf documents, urls that contain pdf's, a text file that contains urls, ioc's from emails and rss feeds. it also perform whitelisting in order to prevent false positives. it uses the files whitelist.dat and the alexa top 1m files.

# Requirements
  - gmail python lib https://github.com/charlierguo/gmail
  - BeautifulSoup lib http://www.crummy.com/software/BeautifulSoup/
  - pdfminer lib https://github.com/euske/pdfminer
  - ElementTree lib http://effbot.org/zone/element-index.htm
  - python-magic lib this can be installed running the following command: apt-get install python-magic 

# Usage
======
```
usage: iocminion.py [-h] [--rss RSS] [--url_file URL_FILE] [--url URL]
                    [--pdf PDF] [--email EMAIL EMAIL] [--write WRITE]

welcome to iocMinion

optional arguments:
  -h, --help           show this help message and exit

Formats supported:
  --rss RSS            process rss url
  --url_file URL_FILE  process text file with urls
  --url URL            process url
  --pdf PDF            process pdf on an url or a pdf on the filesystem. make sure filename doesnt contain spaces
  --email EMAIL EMAIL  looks for iocs on gmail inbox. username and password are required (username pass)
  --write WRITE        write Results to a file

```
# Usecases:
- i would like to get iocs from a blog post i find interesting 
```
python iocminion.py --url http://blog.malwaremustdie.org/2015/06/mmd-0034-2015-new-elf.html
```
- i found a link to a pdf containing iocs i would like to extract ioc's from it.
```
 python iocminion.py  --pdf http://www.welivesecurity.com/wp-content/uploads/2015/04/mumblehard.pdf
```
- i have a list of 40 url's on a txt file and i would like to extract the ioc's of all of those pages of one shot
```
python iocminion.py --url_file urls.txt
```
- i would like to process all ioc's but i would like to save them to a a file.
```
python iocminion.py --url http://blog.malwaremustdie.org/2015/06/mmd-0034-2015-new-elf.html -w outfile.txt
```
