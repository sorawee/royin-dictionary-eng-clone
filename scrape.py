import grequests
import requests
import re
import os
from bs4 import BeautifulSoup
import csv

url = 'http://rirs3.royin.go.th/coinages/websearch.php?Wd=&Mrs={max_results}&Sj=0&Ot=2&Cpr={i}&Pnt={i}'
headers = {'Referer': 'http://rirs3.royin.go.th/coinages/webfind.php'}
max_results = 109152
start = 55970
session = requests.Session()
generator = (grequests.get(url.format(max_results=max_results, i=i), headers=headers)
             for i in range(start, max_results, 10))
pages = grequests.imap(generator, size=5)
for page in pages:
    print(page.url)
    try:
        content_tmp = page.content.decode('TIS-620')
    except UnicodeDecodeError:
        print('have error in encoding; please check')
        content_tmp = page.content.decode('TIS-620', 'replace')
    content = content_tmp.replace('', '“').replace('', '”').replace('', '‘').replace('', '’')
    soup = BeautifulSoup(content, 'html5lib')
    lst = soup.select('table[border="1"]')[0].tbody.contents[1:]
    lst = list(filter(lambda x: x.name == 'tr', lst))
    print(len(lst))
    for row in lst:
        src, dst, reference = filter(lambda x: x.name == 'td', row.contents)
        source, year = reference.font.stripped_strings
        with open('file-{}.tsv'.format(source), 'a') as f:
            wr = csv.writer(f, delimiter='\t')
            wr.writerow([''.join(str(x) for x in src.contents), ''.join(str(x) for x in dst.contents), year])
    page.close()
