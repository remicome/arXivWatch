#
# arXivWatch.py:
#   Surveille les mises à jours sur arXiv (cf. README)
#

#============================================================
subjects = ['math.AP', 'math.KT', 'math.OA', 'math.ST', 'math.DG']
max_results = 100

def is_interesting(entry):
    """ 
    Filtre les entrées intéressantes 

    Argument: une instance ArXivEntry
    Retourne: True si l'entrée est intéressante, False sinon.
    """

    authors = ['E(\.|lmar) Schrohe',
            'V(\.|ictor) Nistor',
            'M(\.|arius) Mantoiu',
            'G(\.|eorges) Skandalis',
            'C(\.|laire) Debord',
            'J(\.|ean)-M(\.|arie) Lescure',
            'P(\.|aulo) Carrillo Rouse',
            'R(\.|ichard) Melrose',
            'A(\.|lain) Connes',
            'A(\.|ndrás) Vasy',
            'D(\.|aniel) Grieser'
            ]

    keywords = ['elliptic', 
            'pseudodifferential', 
            'Fredholm',
            'index', 
            'conical', 
            'groupoid', 
            'microlocal',
            ]

    for aut in authors:
        for entry_aut in entry.authors:
            if re.match(aut, entry_aut):
                return True

    for keyword in keywords:
        if (keyword in entry.title) or (keyword in entry.abstract):
            return True

    return False


# Parameters for the smtp server
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_user = 'dupont@example.com'
smtp_password = 'password'
from_addr = 'dupont@example.com'
to_addr = from_addr

# File which records the date of last query
datefile_path='/var/lib/arXivWatch/arXivWatch'

#============================================================


import requests
from bs4 import BeautifulSoup
import os, time, sys, re

import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from _classes import ArXivEntry

#============================================================
# Reading the last time the script was called by the user
# datefile_path = '%s/%s' % (os.getenv("HOME"), datefile)

timeformat='%d/%m/%Y %H:%M\n'

if os.path.isfile(datefile_path):
    with open(datefile_path, 'r') as f:
        time_of_last_search = time.strptime(f.read(), timeformat)
else:
    time_of_last_search = time.gmtime()
#
#============================================================


#============================================================
# Building the search query
search_query = ''
for i, subject in enumerate(subjects):
    if i > 0:
        search_query += '+OR+'
    search_query += subject

# Calling the api
get_more_entries = True
start = 0

api_call = 'http://export.arxiv.org/api/query'
api_call += '?search_query=%s' % search_query
api_call += '&max_results=%s' % max_results
api_call += '&sortBy=lastUpdatedDate&sortOrder=descending'

kept_entries = []
while get_more_entries:
    api_call_with_offset = api_call + ('&start=%s' % start)
    r = requests.get(api_call_with_offset)

    # Sorting through the entries
    feed = BeautifulSoup(r.content, 'lxml')
    for entry in feed.find_all('entry'):
        parsed_entry = ArXivEntry(entry)
        if parsed_entry.updated > time_of_last_search and is_interesting(parsed_entry):
            kept_entries.append(parsed_entry)
        # Keep searching until we reach entries older than the last search
        get_more_entries = (parsed_entry.updated > time_of_last_search)

    start += max_results
#
#============================================================

if len(kept_entries) == 0:
    exit(1)

#============================================================
# Sending an email with the results
env = Environment(loader=FileSystemLoader(sys.path[0]))

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    """ Filtre Jinja2 pour formatter une date """
    return time.strftime(format, value)
env.filters['datetimeformat'] = datetimeformat


tpl = env.get_template('arXiv-mail.html.jinja')
html = tpl.render(entries=kept_entries).encode('utf8')
msg = MIMEText(html, 'html', 'utf-8')

msg['Subject'] = "Mises à jour arXiv"
msg['From'] = from_addr
msg['To'] = to_addr

with smtplib.SMTP(smtp_server, port=smtp_port) as smtp:
    smtp.ehlo() 
    smtp.starttls() 
    smtp.ehlo() 
    smtp.login(smtp_user, smtp_password)
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
#
#============================================================

#============================================================
# If everything went well, records today's date
with open(datefile_path, 'w') as f:
    f.write(time.strftime(timeformat, time.gmtime()))
#
#============================================================
