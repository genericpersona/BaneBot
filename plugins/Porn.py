# -*- coding: utf-8 -*-

import random

from bs4 import BeautifulSoup
import requests
from twisted.python import log

import plugins.PluginBase as pb

class Porn(pb.CommandPlugin):
  CB_URL = 'http://chaturbate.com/affiliates/api/' + \
           'onlinerooms/?format=json&wm=N6TZA'
  GW_URL = 'https://www.reddit.com/r/{}/new/.json'
  PORN_PIC_URL = 'http://pornpicdumps.com/random'
  PORN_PIC_URL2 = 'http://xxxpicdump.com/random'
  PORN_VID_URL = 'http://www.boyshaveapenisgirlshaveavagina.com/index.php'

  def __init__(self, conf):
    super(Porn, self).__init__(conf)
    random.seed()

  def commands(self):
      return { 'cb': self.cb_online
             , 'gw': self.gw
             , 'porn': self.porn
             , 'porn-pic': self.porn_pic
             , 'porn-pic2': self.porn_pic2
             , 'porn-vid': self.porn_vid
             }

  def cb_online(self, args, irc):
    '''(cb [username]) --
        Returns true if the given Chaturbate
        user is online and false otherwise.
        Provided by FrankieDux.
    '''
    if not args:
        return u'[Error]: Missing cam slut\'s username'
    else:
        un = args[0]
        
    try:
        heads = {"User-Agent" : \
                "Mozilla/5.0 (X11; Linux x86_64; rv:34.0) " + \
                "Gecko/20100101 Firefox/34.0"}
        users = requests.get(self.CB_URL, headers=heads).json()
        for user in users:
            if un.lower() == user['username']:
                cb_url = 'https://www.chaturbate.com/{}'.format(un.lower())
                cb_url_short = irc.fact.plugins['URL'].shorten_url(cb_url)
                return u'{} is camming it up at '.format(un) + \
                       u'{}. Don\'t forget to tip, bb'.format(cb_url_short)

        return u'{} is not currently slutting it up for tokens.  Don\'t beg!'.format(un)
    except:
        return u'[Error]: Unable to contact Chaturbate API'

  def gw(self, args, irc):
    '''(gw [aw/asians]
           [bb/bigboobs]
           [bbw]
           [ch/gonewildchubby]
           [gw/gonewild]
           [gwc/gonewildcurvy]
           [iw/indiansgonewild]
           [lw/latinas] 
           [oo/onoff]
       )
       -- Retrieves the latest picture URL from a given
          reddit gone wild sub-reddit.
          Defaults to bbw.
          Provided by FrankieDux.
    '''
    if not args:
        url = self.GW_URL.format('bbw')
    else:
        sr = self.gw_sr_url(args[0])
        if sr:
            url = self.GW_URL.format(sr)
        else:
            return u'[Error]: Invalid sub-reddit specified'

        heads   = {"User-Agent" : \
                "Mozilla/5.0 (X11; Linux x86_64; rv:34.0) " + \
                "Gecko/20100101 Firefox/34.0"}
        try:
            r = requests.get(url, headers=heads)

            if r.status_code != 200:
                return u'[Error]: /r/{} does not exist'.format(args[0])

            for sd in r.json()['data']['children']:
                title = sd['data']['title']
                if not ('[m]' in title.lower() or '(m)' in title.lower()):
                    return u'{} | {}'.format(title, sd['data']['url'])
        except ValueError:
            return u'[Error]: /r/{} did not have images'.format(args[0])
        except:
            return u'[Error]: Cannot retrieve latest sub-reddit smut'

  def gw_sr_url(self, sr):
    '''Given a sub-reddit, return the associated
    URL for retrieving the latest submissions.
    '''
    urls = { 'aw': 'asiansgonewild'
           , 'bb': 'bigboobsgw'
           , 'bbw': 'bbw'
           , 'ch': 'gonewildchubby'
           , 'gw': 'gonewild'
           , 'gwc': 'gonewildcurvy'
           , 'iw': 'indiansgonewild'
           , 'lw': 'latinasgw'
           , 'oo': 'onoff'
           }
    if sr in urls:
        return urls[sr]
    else:
        return sr

  def porn(self, args, irc):
    '''(porn [-v/--video]) -- 
    Return a link to random porn pic if no argument is provided or 
    a video with the -v/--video switch
    '''
    if '-v' in args or '--video' in args:
        return self.porn_vid(args, irc)
    else:
        if random.random() < .5:
            return self.porn_pic(args, irc)
        else:
            return self.porn_pic2(args, irc)

  def porn_pic(self, args, irc):
    '''Return a link to a random porn pic from pornpicdumps
    '''
    try:
        r = requests.get(self.PORN_PIC_URL)
        if not r.status_code == 200:
            return u'[Error]: Invalid response from porn pic API'

        soup = BeautifulSoup(r.text)
        imgs = soup.find('div', id='result').find_all('img')
        return random.choice(map(lambda x: x['src'], imgs))
    except:
        log.err('[Error]: {}'.format(sys.exc_info()[0]))
        return u'[Error]: Cannot contact porn pic API.'

  def porn_pic2(self, args, irc):
    '''Return a link to a random porn pic from xxxpicdump
    '''
    try:
        r = requests.get(self.PORN_PIC_URL2)
        if not r.status_code == 200:
            return u'[Error]: Invalid response from porn pic API'

        soup = BeautifulSoup(r.text)
        img = soup.find('div', {'class': 'img-holder'}).find('img')
        return img['src']
    except:
        log.err('[Error]: {}'.format(sys.exc_info()[0]))
        return u'[Error]: Cannot contact porn pic API.'

  def porn_vid(self, args, irc):
    '''Return a link to a random porn video from boyshaveapenisgirlshaveavagina
    '''
    try:
        r = requests.get(self.PORN_VID_URL)

        if not r.status_code == 200:
            return u'[Error]: Invalid response from porn video API'

        soup = BeautifulSoup(r.text)
        return soup.find('div', id='clicker').find('a')['href']
    except:
        log.err('[Error]: {}'.format(sys.exc_info()[0]))
        return u'[Error]: Cannot contact porn video API.'
