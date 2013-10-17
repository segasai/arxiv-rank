# Arxiv filter and sorter

The goal of this program is to allow to filter and sort arxiv rss listings
by keywords and authors. The only thing you need to do is to write down 
two files keywords_list and authors_list and the start the application

 python  app.py

Then if you go to http://localhost:5000/ you'll see the list of arxiv
articles sorted by the how many matched keywords and matched authors you get


## Requirements:

feedparser nltk BeautifulSoup flask jinja2 numpy packages

All of them can be installed by doing 

pip install 
