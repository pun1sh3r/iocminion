#!/usr/bin/python
import re
from netaddr import IPNetwork, IPAddress
import urllib2
import csv
from cStringIO import StringIO
import pprint
import sys
import os
import datetime
from collections import defaultdict
import argparse
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

try:
    import gmail
except ImportError:
    print "gmail lib not installed see: https://github.com/charlierguo/gmail"

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    print "BeautifulSoup not installed see: http://www.crummy.com/software/BeautifulSoup/ "
try:
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
except ImportError as ex:
    print "pdfminer not installed see: https://github.com/euske/pdfminer %s" % (ex)

try:
    import xml.etree.ElementTree as ET
except ImportError:
    print "ElementTree not installed. see: http://effbot.org/zone/element-index.htm"

try:
    import magic
except ImportError:
    print "python-magic not installed. run apt-get install python-magic "


class iocMinion():
    def __init__(self):
        self.md5Regex = "\\b[a-fA-F0-9]{32}\\b"
        self.sha1Regex = "\\b[a-fA-F0-9]{40}\\b"
        self.sha256Regex = "\\b[a-fA-F0-9]{64}\\b"
        self.ipRegex = "\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\[?\.\]?){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):?\d+?\\b"
        self.domainRegex = "\\b([A-Z0-9_\-\.]+\[?\.\]?(?:XN--CLCHC0EA0B2G2A9GCD|XN--HGBK6AJ7F53BBA|XN--HLCJ6AYA9ESC7A|XN--11B5BS3A9AJ6G|XN--MGBERP4A5D4AR|XN--XKC2DL3A5EE0H|XN--80AKHBYKNJ4F|XN--XKC2AL3HYE2A|XN--LGBBAT1AD8J|XN--MGBC0A9AZCG|XN--9T4B11YI5A|XN--MGBAAM7A8H|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--YFRO4I67O|XN--YGBI2AMMX|XN--3E0B707E|XN--JXALPDLP|XN--KGBECHTV|XN--OGBPF8FL|XN--0ZWM56D|XN--45BRJ9C|XN--80AO21A|XN--DEBA0AD|XN--G6W251D|XN--GECRJ9C|XN--H2BRJ9C|XN--J6W193G|XN--KPRW13D|XN--KPRY57D|XN--PGBS0DH|XN--S9BRJ9C|XN--90A3AC|XN--FIQS8S|XN--FIQZ9S|XN--O3CW4H|XN--WGBH1C|XN--WGBL6A|XN--ZCKZAH|XN--P1AI|XN--NGBC5AZD|XN--80ASEHDB|XN--80ASWG|XN--UNUP4Y|MUSEUM|TRAVEL|AERO|ARPA|ASIA|COOP|INFO|JOBS|MOBI|BIZ|CAT|COM|EDU|GOV|INT|MIL|NET|ORG|PRO|TEL|XXX|AC|AD|AE|AF|AG|AI|AL|AM|AN|AO|AQ|AR|AS|AT|AU|AW|AX|AZ|BA|BB|BD|BE|BF|BG|BH|BI|BJ|BM|BN|BO|BR|BS|BT|BV|BW|BY|BZ|CA|CC|CD|CF|CG|CH|CI|CK|CL|CM|CN|CO|CR|CU|CV|CW|CX|CY|CZ|DE|DJ|DK|DM|DO|DZ|EC|EE|EG|ER|ES|ET|EU|FI|FJ|FK|FM|FO|FR|GA|GB|GD|GE|GF|GG|GH|GI|GL|GM|GN|GP|GQ|GR|GS|GT|GU|GW|GY|HK|HM|HN|HR|HT|HU|ID|IE|IL|IM|IN|IO|IQ|IR|IS|IT|JE|JM|JO|JP|KE|KG|KH|KI|KM|KN|KP|KR|KW|KY|KZ|LA|LB|LC|LI|LK|LR|LS|LT|LU|LV|LY|MA|MC|MD|ME|MG|MH|MK|ML|MM|MN|MO|MP|MQ|MR|MS|MT|MU|MV|MW|MX|MY|MZ|NA|NC|NE|NF|NG|NI|NL|NO|NP|NR|NU|NZ|OM|PA|PE|PF|PG|PH|PK|PL|PM|PN|PR|PS|PT|PW|PY|QA|RE|RO|RS|RU|RW|SA|SB|SC|SD|SE|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SR|ST|SU|SV|SX|SY|SZ|TC|TD|TF|TG|TH|TJ|TK|TL|TM|TN|TO|TP|TR|TT|TV|TW|TZ|UA|UG|UK|US|UY|UZ|VA|VC|VE|VG|VI|VN|VU|WF|WS|YE|YT|ZA|ZM|ZW))(?:\s|$)\\b"

    def sendEmail(self, recipients, body, subject, files=None):
        print "sendEmail"
        try:

            s = smtplib.SMTP('smtp.relay.com')
            s.set_debuglevel(1)
            if files:
                msg = MIMEMultipart()
                msg.attach(MIMEText(body))
                with open(files, 'rb') as f:
                    part = MIMEApplication(f.read())
                    part.add_header('Content-Disposition', 'attachment', filename="%s" % files)
                    msg.attach(part)
            else:
                msg = MIMEText(body)
            sender = 'test@test.com'
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ", ".join(recipients)

            s.sendmail(sender, recipients, msg.as_string())
            s.close()

        except smtplib.SMTPException as e:
            print "error: %s" % e

    def parse_gmail(self, username, passwd, ioc_data):

        try:
            emailData = defaultdict(set)
            g = gmail.login(username, passwd)
            if (g.logged_in):
                print "sucessful login..."
                today = datetime.date.today().strftime("%Y-%m-%d")
                daysBack = datetime.date.today() - datetime.timedelta(days=2)
                emails = g.inbox().mail(before=datetime.date.today(), after=daysBack, unread=True)
                for e in range(0, len(emails)):
                    try:
                        emails[e].fetch()
                        content = emails[e].body
                        subject = re.sub('(^\s|re:\s+|\r\n|fwd:\s+)', '', emails[e].subject, flags=re.IGNORECASE)
                        ioc_data[subject]['hashes'] = set()
                        ioc_data[subject]['ip'] = set()
                        ioc_data[subject]['domain'] = set()
                        self.get_hashes(content, ioc_data[subject]['hashes'], self.md5Regex)
                        self.get_ip(content, ioc_data[subject]['ip'])
                        self.get_domain(content, ioc_data[subject]['domain'])
                        self.get_hashes(content, ioc_data[subject]['hashes'], '\\b[a-fA-F0-9]{64}\\b')
                        self.get_hashes(content, ioc_data[subject]['hashes'], '\\b[a-fA-F0-9]{40}\\b')
                    except Exception as ex:
                        continue
                print "emails found: %s" % len(emails)
            else:
                sys.exit()
        except gmail.exceptions.AuthenticationError:
            print "auth error"
            sys.exit()

    def print_iocs(self, ioc_data, toFile, outFile, format):
        fileOut = []
        
        today = datetime.date.today().strftime("%Y-%m-%d")
        for key, values in ioc_data.iteritems():
            key = key.replace('\n', '')
            for k, v in values.iteritems():
                if str(type(v)) == "<type 'NoneType'>":
                    continue
                for j in v:
                    if (len(j) > 1):
                        matchip = self.val_ip(j)
                        matchDom = self.val_domain(j)
                        matchhash = self.val_hash(j)
                        if (matchhash == True ):
                            fileOut.append("%s" % (j.encode('utf-8').lower()))
                        elif (matchip == True):
                            isinWl = self.isInWhitelist(j)
                            if (isinWl == True):
                                continue
                            else:
                                fileOut.append("%s" % (j.encode('utf-8').lower()))
                        else:
                            isinWl = self.isInWhitelist(j.lower())
                            if (isinWl == True):
                                continue
                            else:
                                fileOut.append("%s" % (j.encode('utf-8').lower()))

        if toFile == True:
            print "writing to file...."
            with open(outFile, 'w') as fd:
                fd.write('\n'.join(fileOut))
        else:
            print '\n'.join(fileOut)


    def get_hashes(self, html, ioc_data, regex):
        if (str(type(html)) == "<type 'str'>"):
            hashes = re.findall(r'%s' % (regex), html)
            for h in hashes:
                ioc_data.add(h)
        else:
            for i in html.findAll(text=re.compile(r'%s' % (regex), re.I)):
                hashes = re.search(r'%s' % (regex), i)
                ioc_data.add(hashes.group(0))

    def parse_rss(self, url, ioc_data):
        url = self.do_request(url)
        xmlRes = ET.fromstring(url)
        urlfile = open('url_proccesed.txt', 'a+')
        urlContent = urlfile.read().split('\n')
        for child in xmlRes.iter('item'):
            desc = ''
            for ch2 in child:
                if ch2.tag == 'link':
                    url = ch2.text
                if ch2.tag == 'description':
                    desc = ch2.text
            print url
            ioc_data[url]['hashes'] = set()
            ioc_data[url]['ip'] = set()
            ioc_data[url]['domain'] = set()
            ioc_data[url]['description'] = desc
            res = self.do_request(url)
            try:
                isPdf = re.match(r'^%PDF', res)
            except Exception as ex:
                print "pdf exception %s" % (ex)

            if (isPdf):
                print "is pdf"
                data = self.parse_pdf(res)
                self.get_hashes(data, ioc_data[url]['hashes'], self.md5Regex)
                self.get_ip(html, ioc_data[url]['ip'])
                self.get_domain(html, ioc_data[url]['domain'])
                self.get_hashes(html, ioc_data[url]['hashes'], '\\b[a-fA-F0-9]{64}\\b')
                self.get_hashes(html, ioc_data[url]['hashes'], '\\b[a-fA-F0-9]{40}\\b')
            else:
                try:
                    html = BeautifulSoup(res)
                    self.get_hashes(html, ioc_data[url]['hashes'], self.md5Regex)
                    self.get_ip(html, ioc_data[url]['ip'])
                    self.get_domain(html, ioc_data[url]['domain'])
                    self.get_hashes(html, ioc_data[url]['hashes'], '\\b[a-fA-F0-9]{64}\\b')
                    self.get_hashes(html, ioc_data[url]['hashes'], '\\b[a-fA-F0-9]{40}\\b')
                except Exception as ex:
                    print ex


    def get_domain(self, html, ioc_data):
        if (str(type(html)) == "<type 'str'>"):
            domain = re.findall(r'%s' % (self.domainRegex), html, re.I | re.S)
            for d in domain:
                ioc_data.add(d.lower())
        else:
            domain = re.findall(r'%s' % (self.domainRegex), str(html), re.I | re.S)
            for i in html.findAll(name='body', text=re.compile(r'%s' % (self.domainRegex), re.I)):
                domain = re.search(r'%s' % (self.domainRegex), i, re.I)
                domain = re.sub(r'(\[|\])', '', domain.group(0))
                ioc_data.add(domain.lower())

    def get_ip(self, html, ioc_data):
        if (str(type(html)) == "<type 'str'>"):
            ip = re.findall(r'%s' % (self.ipRegex), html)
            for i in ip:
                i = re.sub(r'(\[|\]|:.*)', '', i)
                ioc_data.add(i)
        else:
            for i in html.findAll(text=re.compile(r'%s' % (self.ipRegex))):
                ip = re.search(r'%s' % (self.ipRegex), i)
                ioc_data.add(ip.group(0))

    def do_request(self, url):
        try:
            browser = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=0))
            browser.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0')]
            req = browser.open(url)
            res = req.read()
            req.close()
            return res
        except urllib2.HTTPError, e:
            print "http error code:%s\turl:%s " % (e.code, url)
            # sys.exit()


    def val_domain(self, content):
        match = re.findall(r'%s' % (self.domainRegex), content, re.I)
        if (match):
            return True
        else:
            return False

    def val_ip(self, content):
        match = re.findall(r'%s' % (self.ipRegex), content)
        if (match):
            return True
        else:
            return False

    def val_hash(self, content):
        matchsha1 = re.findall(r'%s' % (self.sha1Regex), content, re.I)
        matchmd5 = re.findall(r'%s' % (self.md5Regex), content, re.I)
        matchsha256 = re.findall(r'%s' % (self.sha256Regex), content, re.I)
        if (matchmd5):
            return True
        elif (matchsha1):
            return True
        elif (matchsha256):
            return True
        else:
            return False

    def isInWhitelist(self, data):
        matchip = re.findall(r'%s' % (self.ipRegex), data)
        if (matchip):
            with open('whitelist.dat', 'rU') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                for row in csvreader:
                    if data:
                        try:
                            if IPAddress(data) in IPNetwork(row[0]) or IPAddress(data).is_private():
                                return True
                        except Exception as ex:
                            continue
        else:
            with open('top-1m.csv', 'rb') as csvfile1:
                csvreader = csv.reader(csvfile1, delimiter=',')
                for row in csvreader:
                    flag = data.find(row[1])
                    if flag != -1:
                        return True

    def parse_pdf(self, data):
        ms = magic.open(magic.MAGIC_NONE)
        ms.load()
        tempFile = 'temp.pdf'

        if re.match(r'https?:\/\/.*\.pdf', data):
            res = self.do_request(data)
            try:
                if 'PDF' in ms.buffer(res):
                    with open(tempFile, 'wb') as pdfDoc:
                        pdfDoc.write(res)
                    fp = file(tempFile, 'rb')
                    rsrcmgr = PDFResourceManager()
                    retstr = StringIO()
                    codec = 'utf-8'
                    laparams = LAParams()
                    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    password = ""
                    maxpages = 0
                    caching = True
                    pagenos = set()
                    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                                  check_extractable=True):
                        interpreter.process_page(page)
                    fp.close()
                    device.close()
                    str1 = retstr.getvalue()
                    retstr.close()
                    os.unlink(tempFile)
                    return str1
                else:
                    print "test"
                    print "File not a pdf..."
                    sys.exit()
            except Exception as ex:
                print ex
        else:
            fd = open(data,'rb').read()
            if 'PDF' in ms.buffer(fd):
                fp = file(data, 'rb')
                rsrcmgr = PDFResourceManager()
                retstr = StringIO()
                codec = 'utf-8'
                laparams = LAParams()
                device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                password = ""
                maxpages = 0
                caching = True
                pagenos = set()

                for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                              check_extractable=True):
                    interpreter.process_page(page)
                    # print page
                fp.close()
                device.close()
                str1 = retstr.getvalue()
                retstr.close()
                return str1
            else:
                print "File not a pdf..."
                sys.exit()


def main():
    ioc_data = defaultdict(dict)

    today = datetime.date.today().strftime("%Y-%m-%d")
    iocObj = iocMinion()
    options = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="welcome to iocMinion")
    group = options.add_argument_group("Formats supported")
    group.add_argument('--rss', help='process rss url', nargs=1, required=False)
    group.add_argument('--url_file', help='process text file with urls', nargs=1, required=False)
    group.add_argument('--url', help='process url', nargs=1, required=False)
    group.add_argument('--pdf',
                       help='process pdf on an url or a pdf on the filesystem. make sure filename doesnt contain spaces',
                       nargs=1, required=False)
    group.add_argument('--email',
                       help='looks for iocs on gmail inbox. username and password are required (username pass)',
                       nargs=2)
    group.add_argument('-w', dest='write', help='write Results to a file', nargs=1, required=False)
    group.add_argument('--format', help='output format', choices=('csv', 'json'), nargs=1, required=False)
    args = options.parse_args()

    if args.rss:
        print "processing the following rss feed: %s:" % args.rss[0]
        iocObj.parse_rss(args.rss[0], ioc_data)
        pprint.pprint(ioc_data)
    if args.url_file:
        print "processing the following url file: %s" % args.url_file[0]
        with open(args.url_file[0], 'r') as fd:
            for url in fd:
                ioc_data[url]['hashes'] = set()
                ioc_data[url]['ip'] = set()
                ioc_data[url]['domain'] = set()
                try:
                    html = BeautifulSoup(iocObj.do_request(url))
                    iocObj.get_hashes(html, ioc_data[url]['hashes'], '\\b[a-fA-F0-9]{32}\\b')
                    iocObj.get_hashes(html, ioc_data[url]['hashes'], '\\b[a-fA-F0-9]{64}\\b')
                    iocObj.get_hashes(html, ioc_data[url]['hashes'], '\\b[a-fA-F0-9]{40}\\b')
                    iocObj.get_ip(html, ioc_data[url]['ip'])
                    iocObj.get_domain(html, ioc_data[url]['domain'])
                except Exception as ex:
                    print ex
    if args.url:
        print "processing the following url file: %s" % args.url[0]
        try:
            ioc_data[args.url[0]]['hashes'] = set()
            ioc_data[args.url[0]]['ip'] = set()
            ioc_data[args.url[0]]['domain'] = set()
            html = BeautifulSoup(iocObj.do_request(args.url[0]))
            iocObj.get_hashes(html, ioc_data[args.url[0]]['hashes'], '\\b[a-fA-F0-9]{32}\\b')
            iocObj.get_hashes(html, ioc_data[args.url[0]]['hashes'], '\\b[a-fA-F0-9]{64}\\b')
            iocObj.get_hashes(html, ioc_data[args.url[0]]['hashes'], '\\b[a-fA-F0-9]{40}\\b')
            iocObj.get_ip(html, ioc_data[args.url[0]]['ip'])
            iocObj.get_domain(html, ioc_data[args.url[0]]['domain'])
        except Exception as ex:
            print ex
    if args.pdf:
        print 'procesing pdf...'
        ioc_data[args.pdf[0]]['hashes'] = set()
        ioc_data[args.pdf[0]]['ip'] = set()
        ioc_data[args.pdf[0]]['domain'] = set()
        data = iocObj.parse_pdf(args.pdf[0])
        iocObj.get_hashes(data, ioc_data[args.pdf[0]]['hashes'], '\\b[a-fA-F0-9]{32}\\b')
        iocObj.get_hashes(data, ioc_data[args.pdf[0]]['hashes'], '\\b[a-fA-F0-9]{64}\\b')
        iocObj.get_hashes(data, ioc_data[args.pdf[0]]['hashes'], '\\b[a-fA-F0-9]{40}\\b')
        iocObj.get_ip(data, ioc_data[args.pdf[0]]['ip'])
        iocObj.get_domain(data, ioc_data[args.pdf[0]]['domain'])

    if args.email:
        iocObj.parse_gmail(args.email[0], args.email[1], ioc_data)

    if args.write and args.format:
        iocObj.print_iocs(ioc_data, True, args.write[0], args.format[0])
    else:
        iocObj.print_iocs(ioc_data, False, None, args.format[0])


if __name__ == '__main__':
    main()
