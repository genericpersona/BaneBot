# -*- coding: utf-8 -*-

import json
import re
import time
import traceback
import sys

from bs4 import BeautifulSoup
import pafy
import requests
from twisted.python import log

import plugins.PluginBase as pb

class URL(pb.LinePlugin, pb.CommandPlugin):
  GOOGLE_SHORTEN = 'https://www.googleapis.com/urlshortener/v1/url'
  URL_RE = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
  YT_RE = re.compile(r'^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$')
  YT_SEARCH = 'https://www.youtube.com/results?search_query={}'

  def __init__(self, conf):
    super(URL, self).__init__(conf)

  def commands(self):
    return { 'shorten': self.shorten
           , 'unshorten': self.unshorten
           , 'yt': self.ytSearch
           }

  def hasResponse(self, msg, irc):
    '''Checks a line of input for the following:

        - A URL (could be many)
            -- If YouTube, print out data
            -- Otherwise, print out the title
    '''
    # Look for all URLs in the msg
    urls = self.URL_RE.findall(msg)
    if not urls:
        return False

    # Check each one and build a response
    responses = []
    for url in urls:
        if self.YT_RE.match(url) is not None:
            responses.append(self.youtube_data(url))
        else:
            responses.append(self.title(url))

        if len(url) > self.max_url_len:
            responses.append(u'Shortened: {}'.format(self.shorten_url(url)))

        log.msg('Processed URL: {}'.format(url))

    # Only get True responses
    responses = filter(bool, responses)
    if responses:
        irc.response = u'\n'.join(responses)
        return True
    else:
        return False

  def reachable_url(self, url):
    '''True if the URL passed in can be contacted without a server
    or client error status code.
    '''
    try:
        return 200 <= requests.head(url).status_code < 400 
    except:
        return False

  def shorten(self, args, irc):
    '''Shorten a single URL
    '''
    try:
        url = self.URL_RE.findall(u' '.join(args))[0]
    except IndexError:
        return '[Error]: Invalid URL'

    return self.shorten_url(url)

  def shorten_url(self, url):
    '''Return a shortened version of a URL passed in
    using Google's URL shortening service.
    '''
    headers = {'Content-Type': 'application/json'
              , 'User-Agent': 'Bane Bot'
              }
    data = json.dumps({'longUrl': url})
    try:
      r = requests.post(self.GOOGLE_SHORTEN, headers=headers, data=data)
    except:
      return u'[Error]: Invalid URL'

    if r.status_code != 200:
      return u'[Error]: Invalid status code {}'.format(r.status_code)
    else:
      return r.json()['id']

  def title(self, url):
    '''Return the title of a passed in URL
    '''
    try:
        soup = BeautifulSoup(requests.get(url, verify=False).text)
        if soup.title is None:
            return
        url_title = u' '.join(soup.title.text.strip().\
                                replace(u'\n', u' ').split())
        return url_title
    except:
        log.msg('[Error]: title {}'.format(traceback.format_exc()))

  def unshorten(self, args, irc):
    '''Method to handle the command for unshortening a URL
    '''
    try:
        url = self.URL_RE.findall(u' '.join(args))[0]
    except IndexError:
        return u'[Error]: Invalid URL'

    try:
        return self.unshorten_url(url)
    except:
        irc.pm = True
        return u'[Error]: Couldn\'t reach URL'

  def unshorten_url(self, url):
    '''Follow the redirects until the full URL is found.
    Code from: http://ow.ly/ttH5j
    '''
    try:
        real_url = requests.head(url, timeout=100.0,
                headers={'Accept-Encoding': 'identity'})
        return real_url.headers.get('location', url)
    except:
        pass

  def youtube_data(self, url):
    '''Return the video title, duration, and view count for a YouTube URL.
    '''
    try:
        video = pafy.new(url)
        title = video.title
        duration = video.duration
        views = video.viewcount

        return u'Title: {} | Duration: {} | Views: {:,}'.format(\
                                title, duration, views)
    except:
        log.err('[Error]: pafy {}'.format(sys.exc_info()[0]))

  def ytSearch(self, args, irc):
      '''yt [search term(s)] -- Search YouTube and return the first result
      '''
      try:
        if not args:
            return u'[Error]: Missing YouTube search terms'

        terms = u'+'.join(args)
        r = requests.get(self.YT_SEARCH.format(terms))

        soup = BeautifulSoup(r.text)
        result = soup.find('div', {'class': 'yt-lockup-content'}).find('a')['href']
        url = u'https://youtube.com{}'.format(result)
        return u'{} | {}'.format(url, self.youtube_data(url))
      except:
        log.err('[Error]: yt {}'.format(sys.exc_info()[0]))
        return u'[Error]: Could not contact YouTube'
