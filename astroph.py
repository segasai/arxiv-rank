import feedparser
import nltk
import sys
import numpy as np
import config
from nltk.stem.porter import PorterStemmer
if int(sys.version[0]) >= 3:
    from bs4 import BeautifulSoup
    Parser = BeautifulSoup
else:
    import BeautifulSoup
    Parser = BeautifulSoup.RobustHTMLParser

nltk_ver = tuple([int(_) for _ in nltk.__version__.split('.')])
if nltk_ver >= (3, 2, 2):
    stem = PorterStemmer().stem
else:
    stem = PorterStemmer().word_stem


def get_keys():
    fp = open('keyword_list', 'r')
    keys = []
    origkeys = []
    for l in fp:
        fullstr = l.rstrip()
        if len(fullstr) == 0:
            continue
        words = nltk.wordpunct_tokenize(fullstr)
        #fullstr.split(' ')
        key1 = tuple([stem(_).lower() for _ in words])
        keys.append(key1)
        origkeys.append(fullstr)
    return keys, origkeys


def get_authors():
    fp = open('author_list', 'r')
    keys = []
    for l in fp:
        word = l.rstrip()
        keys.append(word)
    return keys


class article:
    def __init__(self,
                 title=None,
                 authors=None,
                 link=None,
                 tags=[],
                 abstract=None,
                 pdf=None):
        self.title = title
        self.authors = authors
        self.link = link
        self.tags = tags
        self.abstract = abstract
        self.score = len(self.tags)
        self.pdf = pdf

    def printer(self, num):
        abstract = self.abstract
        authors = self.authors
        link = self.link
        title = self.title
        pdf = self.pdf
        tags = ''

        if len(self.tags) > 0:
            for k in self.tags:
                tags = tags + '<div class="tag">%s</div>' % k
        if len(tags) == 0:
            tags = ''
        toggle = 'toggle expanded'
        onclick = ""
        if self.score == 0:
            style = 'score0'
            toggle = 'toggle hidden'
            onclick = str.format(
                """onclick="toggle('abs#{num}','absX#{num}');" """, **locals())
        if self.score == 1:
            style = 'score1'
        if self.score >= 2:
            style = 'score2'

        ret = str.format(
            '''
	<div id="art#{num}" class="art {style}">
		<div id="tag#{num}" class="tag {style}">{tags}</div>
		<div id="title#{num}" class="title {style}"><h2><a href="{link}">{title}</a></h2></div>
		<div id="aut#{num}" class="auth {style}">{authors}</div>
		<div id="abs#{num}" class="abs {style} box {toggle}" {onclick}></div>
		<div id="absX#{num}" class="abs {style} text {toggle}">{abstract}</div>
		<div id="pdflink#{num}" class="pdflink {style}"><a href="{pdf}">PDF</a></div>
	</div><hr>
			''', **locals())
        return ret


class adder:
    def __init__(self):
        self.arts = []

    def add(self, art):
        self.arts.append(art)

    def argsort(self):
        return np.argsort([-_.score for _ in self.arts])

    def printer(self):
        res = ''
        for i in self.argsort():
            res += self.arts[i].printer(i)
        return res


def doit():

    keys, origkeys = get_keys()
    watch_authors = get_authors()

    zz = feedparser.parse(config.rssurl)
    nentries = len(zz['entries'])

    BigRes = adder()

    for i in range(nentries):
        curent = zz['entries'][i]
        ngramlist = []
        maxNgram = 3  # maximum number of words in the phrase allowed
        for curtext in [curent.title, curent.summary]:
            tokens = nltk.wordpunct_tokenize(curtext)
            stemlowtokens = [stem(_).lower() for _ in tokens]
            x = 1
            for x in range(1, maxNgram + 1):
                ngramlist = ngramlist + list(nltk.ngrams(stemlowtokens, x))

        ngrams = set(ngramlist)

        matches = []
        author_matches = []
        for _i, k in enumerate(keys):
            if k in ngrams:
                matches.append(origkeys[_i])

        authorshtml = BeautifulSoup(curent.author, 'html.parser')
        authors = [_.contents[0] for _ in authorshtml.findAll('a')]
        # for cura in authors:
        #	tokens = nltk.word_tokenize(cura)
        #	tokens = [ _.lower() for _ in tokens]
        authors = [
            set([__.lower() for __ in nltk.word_tokenize(_)]) for _ in authors
        ]

        for _ in watch_authors:
            if any([str.lower(_) in __ for __ in authors]):
                author_matches.append(_)

        if len(matches) > 0:
            1
            # print 'KEYWORD',matches, curent.title, curent.link
        else:
            if len(author_matches) > 0:
                1
                # print 'AUTHOR',author_matches, curent.title, curent.link
        BigRes.add(
            article(title=curent.title,
                    abstract=curent.summary,
                    authors=curent.author,
                    tags=matches + author_matches,
                    link=curent.link,
                    pdf=curent.link.replace('abs', 'pdf')))

    return BigRes.printer()
