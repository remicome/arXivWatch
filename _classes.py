# class arXivEntry:
#   Traite les données renvoyées par le feed Atom, pour pouvoir ensuite être affichées facilement par le template

import re
import time

class ArXivEntry:
    def __init__(self, entry):
        self.title = entry.title.string
        self.abstract_page = entry.id.string
        self.id = re.search('http://arxiv.org/abs/(.*)', self.abstract_page).group(1)

        self.pdf = self._get_pdf_link(entry)
        self.abstract = entry.summary.string

        self.authors = []
        for author in entry.find_all('author'):
            self.authors.append(author.find('name').string)

        self.updated = time.strptime(entry.updated.string, '%Y-%m-%dT%H:%M:%SZ')
        self.published = time.strptime(entry.published.string, '%Y-%m-%dT%H:%M:%SZ')


    @staticmethod
    def _get_pdf_link(entry):
        for link in entry.find_all('link'):
            if link.has_attr('title') and link['title'] == 'pdf':
                return link['href']
        return None     # This shouldn't happen as the pdf link is always present as per arXiv documentation
