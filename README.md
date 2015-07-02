# iocminion
=======
Just another tool to extract IOC's from files. this tool has the capability to extract IOC's from the following sources: pdf documents, urls that contain pdf's, a text file that contains urls, ioc's from emails and rss feeds. 

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
