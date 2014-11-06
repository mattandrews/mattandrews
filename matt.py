from time import mktime
from datetime import datetime
import feedparser
import filters
from flask import Flask, render_template
from flask.ext.cache import Cache
from werkzeug.contrib.fixers import ProxyFix

import default_settings

app = Flask(__name__)

cache = Cache(config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DEFAULT_TIMEOUT': default_settings.DEFAULT_CACHE,
    'CACHE_DIR': default_settings.CACHE_DIR,
    'CACHE_THRESHOLD': 10
})
cache.init_app(app)

static_url = default_settings.STATIC_URL
now = datetime.now()

@cache.cached(timeout=2592000, key_prefix='all_writing') # 1 month
def get_rss_content():
    feeds = ['http://www.theguardian.com/profile/matt-andrews/rss', 'http://www.threechords.org/blog/feed/']
    articles = []
    for f in feeds:
        response = feedparser.parse(f)

        for item in response['entries']:
            pub_date = datetime.fromtimestamp(mktime(item['published_parsed']))
            articles.append({
                'date': pub_date,
                'title': item['title'],
                'summary': item['summary'],
                'link': item['link']
            })

    if not articles:
        return False

    return sorted(articles, key=lambda k: k['date'], reverse=True)

@app.route("/")
@cache.cached() # 1 month
def homepage():

    talks = [
        {
            'title':    'Building websites using HTML, CSS and JavaScript',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2014, 9, 3),
            'end':      datetime(2014, 9, 24),
            'link':     'http://www.theguardian.com/guardian-masterclasses/building-websites-html-css-javascript-course'
        },
        {
            'title':    'Building websites using HTML, CSS and JavaScript',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2014, 4, 16),
            'end':      datetime(2014, 5, 7),
            'link':     'http://www.theguardian.com/guardian-masterclasses/building-websites-html-css-javascript-course'
        },
        {
            'title':    'How to work with web developers',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2014, 4, 28),
            'link':     'http://www.theguardian.com/guardian-masterclasses/what-developers-wish-you-knew-matt-andrews-digital-course'
        },
        # bastards
        # {
        #     'title':    'Building for the web: Intermediate coding',
        #     'subtitle': 'Guardian Masterclass',
        #     'start':    datetime(2014, 6, 21),
        #     'end':      datetime(2014, 6, 22),
        #     'link':     'http://www.theguardian.com/guardian-masterclasses/building-for-the-web-intermediate-coding-digital-course'
        # },
        {
            'title':    'Building websites using HTML, CSS and JavaScript',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2014, 3, 6),
            'end':      datetime(2014, 3, 27)
        },
        {
            'title':    'Digital journalism bootcamp',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2014, 2, 25),
            'end':      datetime(2014, 3, 18)
        },
        {
            'title':    'Surviving the multi-device news challenge',
            'subtitle': 'Hacks &amp; Hackers Berlin',
            'start':    datetime(2014, 1, 23)
        },
        {
            'title':    'Building websites using HTML, CSS and JavaScript',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2014, 1, 15),
            'end':      datetime(2014, 2, 5)
        },
        {
            'title':    'Responsive design at the Guardian',
            'subtitle': 'CanvasConf 2013, Birmingham',
            'start':    datetime(2013, 10, 10)
        },
        {
            'title':    'Building websites using HTML, CSS and JavaScript',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2013, 9, 24),
            'end':      datetime(2013, 10, 15)
        },
        {
            'title':    'How web developers work... and what they wish you knew',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2013, 7, 22)
        },
        {
            'title':    'Building websites using HTML, CSS and JavaScript',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2013, 6, 4),
            'end':      datetime(2013, 6, 25)
        },
        {
            'title':    'Responsive design at the Guardian',
            'subtitle': 'Port80 Conference 2013, Newport',
            'start':    datetime(2013, 5, 10)
        },
        {
            'title':    'How to be a digital journalist',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2013, 3, 23),
            'end':      datetime(2013, 3, 24)
        },
        {
            'title':    'Building websites using HTML, CSS and JavaScript',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2013, 2, 27),
            'end':      datetime(2013, 3, 20)
        },
        {
            'title':    'How to be a digital journalist',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2013, 1, 12),
            'end':      datetime(2013, 1, 13)
        },
        {
            'title':    'Building websites using HTML, CSS and JavaScript',
            'subtitle': 'Guardian Masterclass',
            'start':    datetime(2012, 11, 21),
            'end':      datetime(2012, 12, 13)
        }

    ]

    articles = get_rss_content()

    talks = sorted(talks, key=lambda k: k['start'], reverse=True)
    current_talks = []
    past_talks = []
    for t in talks:

        if not 'end' in t:
            t['end'] = t['start']
        if t['end'] < now:
            past_talks.append(t)
        else:
            current_talks.append(t)

    return render_template('template.html', articles=articles, static_url=static_url, past_talks=past_talks, current_talks=current_talks)

# runs on 8002 on prod
@app.route("/cachebust")
def decache():
    with app.app_context():
        cache.clear()
        return 'ok'

app.jinja_env.filters['truncatehtml'] = filters.truncatehtml

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=default_settings.DEBUG)
