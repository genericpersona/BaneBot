# -*- coding: utf-8 -*-

import random
import subprocess as sp
import sys

import bashquote as bq
from bs4 import BeautifulSoup
import requests
from twisted.python import log

import plugins.PluginBase as pb

class Quotes(pb.CommandPlugin):
  BIBLE_URL = 'http://labs.bible.org/api/?passage={}'
  CHUCK_NORRIS_API = 'http://api.icndb.com/jokes/random/'
  COMPLIMENT_URL = 'http://toykeeper.net/programs/mad/compliments'
  EI_URL = 'http://quandyfactory.com/insult/json'
  EUPHEMISM_URL = 'http://toykeeper.net/programs/mad/euphemisms'
  INSULTS_GEN_URL = 'http://www.insultgenerator.org/'
  LI_URL = 'http://ergofabulous.org/luther/'
  NKI_URL = 'http://www.nk-news.net/extras/insult_generator.php'
  PICKUP_LINES_URL = 'http://www.pickuplinegen.com/'
  QURAN_URL = 'http://ayatalquran.com/random'
  SI_URL = 'http://www.pangloss.com/seidel/Shaker/'
  SURREAL_URL = 'http://www.madsci.org/cgi-bin/cgiwrap/~lynn/jardin/SCG'

  def __init__(self, conf):
    super(Quotes, self).__init__(conf)
    self.adj_list = [adj.strip() for adj \
                      in open(self.adjective_file) if adj]
    self.body_list = [part.strip() for part \
                      in open(self.body_file) if part]
    self.insult_list = [insult.strip() for insult \
                        in open(self.insult_file) if insult]
    self.stab_list = [stab.strip() for stab \
                        in open(self.stab_file) if stab]
    random.seed()

  def commands(self):
      return { 'bash-org': self.bash_org
             , 'bible': self.bible_quote
             , 'bq': self.bash_org
             , 'chalkboard': self.chalkboard
             , 'chuck-norris': self.chuck_norris
             , 'cliche': self.cliche
             , 'cnq': self.chuck_norris
             , 'compliment': self.compliment
             , 'ei': self.elizabethan_insult
             , 'euphemism': self.euphemism
             , 'foad': self.foad
             , 'fortune': self.fortune
             , 'homer': self.homer
             , 'insult': self.insult
             , 'li': self.luther_insult
             , 'mormon': self.mormon
             #, 'nki': self.north_korean_insult
             , 'pickup': self.pickup
             , 'si': self.shakespeare_insult
             , 'stab': self.stab
             , 'quran': self.quran
             , 'tao': self.tao
             , 'trolldb': self.trolldb
             }

  def bash_org(self, args, irc):
      '''Return a random quote from bash.org
      '''
      while True:
          quote = bq.BashQuote(bq.getRandomQuoteNum())
          if quote.isExists():
              return quote.getText()

  def bible_quote(self, args, irc):
    '''Obtain a random Bible quote or one from a specific passage
    bible [book chapter:verse]
    '''
    try:
      bible_url = self.BIBLE_URL.format('random' if not args else \
                                        u'+'.join(args))
      bible_url += '&formatting=plain'

      response = requests.get(bible_url)
      if response.status_code == 200:
        return response.text
      else:
        return '[Error]: Invalid response from Bible API.'
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact Bible API.' 

  def chalkboard(self, args, irc):
    '''Random Bart chalkboard line from the opening credits of the Simpsons
    '''
    cmnd = 'fortune chalkboard'
    return sp.check_output(cmnd.split()).split('\n')[0]

  def chuck_norris(self, args, irc):
    '''Random chuck Norris quote
    '''
    # Make a request to the page
    try:
      r = requests.get(self.CHUCK_NORRIS_API)

      # Check for a successful GET
      if not r.status_code == 200:
        return '[Error]: Invalid response from Chuck Norris API.' 

      # Grab the quote now
      quote = str(r.json()['value']['joke']).replace(u'&quot;', u'"')
      return quote
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact Chuck Norris API.' 

  def cliche(self, args, irc):
    '''A platitudinous saying
    '''
    cmnd = 'fortune platitudes'
    cliche = sp.check_output(cmnd.split()).replace(u'\n', u' ')
    return u' '.join(cliche.split())

  def compliment(self, args, irc):
    '''Random compliment. -s/--surreal for a surreal one.
    '''
    # Check if it should be surreal
    if args and args[0] in (u'-s', '--surreal'):
        surreal = True
        args.pop(0)
    else:
        surreal = False

    try:
        if surreal:
            r = requests.get(self.SURREAL_URL)
        else:
            r = requests.get(self.COMPLIMENT_URL)
        if r.status_code != 200:
            log.err('[Error]: Status code of {} for compliment'.format(r.status_code))
            return

        soup = BeautifulSoup(r.text)

        c = soup.find('h2' if surreal else 'h3').text.strip()
        c = u' '.join(c.replace(u'\n', u' ').split())
        if args:
            c = u'{}: {}'.format(args[0], c)

        return c
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact Compliment API.' 

  def elizabethan_insult(self, args, irc):
    '''Elizabethan insult from quandyfactory.com
    '''
    try:
        r = requests.get(self.EI_URL)
        if r.status_code != 200:
            log.err('[Error]: Status code of {} for ei'.format(r.status_code))
            return

        insult = r.json()['insult']
        if args:
            insult = u'{}: {}'.format(args[0], insult)

        return insult
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact Elizabethan Insult API.' 

  def euphemism(self, args, irc):
    '''Random euphemism
    '''
    try:
        r = requests.get(self.EUPHEMISM_URL)
        if r.status_code != 200:
            log.err('[Error]: Status code of {} for euphemism'.format(r.status_code))
            return

        soup = BeautifulSoup(r.text)
        return soup.find('blockquote').text.strip()
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact Euphemism API.' 

  def foad(self, args, irc):
    '''(foad [nickname]) -- https://github.com/adversary-org/foad
    '''
    if not args:
        cmnd = 'foad.py -f random -n {}'.format(irc.sender)
    else:
        cmnd = 'foad.py -f random -s {} -n {}'.format(irc.sender, args[0])

    try:
        return sp.check_output(cmnd.split())
    except sp.CalledProcessError:
        return u'Go fuck yourself, {}'.format(irc.sender) 

  def fortune(self, args, irc):
    off = '-a ' if self.fortune_off else ''
    cmnd = 'fortune {}-s -n {}'.format(off, self.fortune_max_len)
    return u' '.join(\
            sp.check_output(cmnd.split()).replace(u'\n', u' ').split())
 
  def homer(self, args, irc):
    cmnd = 'fortune homer'.format(self.fortune_max_len)
    return u' '.join(\
            sp.check_output(cmnd.split()).replace(u'\n', u' ').split())

  def insult(self, args, irc):
    '''(insult [nickname]) -- Return a random insult.
    '''
    try:
        if random.random() < 0.5:
            i = random.choice(self.insult_list)
        else:
            r = requests.get(self.INSULTS_GEN_URL)
            if not r.status_code == 200:
                log.err('[Error]: Insult status code {}'.format(r.status_code))
                return u'Your mom is a fucking whore, did I ever tell you that?'

            if r.text.startswith('#!/usr/bin/perl'): # Bug in the site
                i = random.choice(self.insult_list)
            else:
                soup = BeautifulSoup(r.text)
                i = soup.find('table').find('td').text.strip()

        if args:
            i = u'{}: {}'.format(args[0], i)

        return u' '.join(i.replace(u'\n', u' ').split())
    except:
        log.err('[Error]: Issue with insults generator {}'.format(sys.exc_info()[0]))
        return u'You should have been a handjob.'

  def luther_insult(self, args, irc):
    '''(li [nickname]) -- Lutheran insult from ergofabulous.org
    '''
    try:
        r = requests.get(self.LI_URL)
        if r.status_code != 200:
            log.err('[Error]: Status code of {} for li'.format(r.status_code))
            return
        
        soup = BeautifulSoup(r.text)
        insult = soup.find('p', {'class': 'larger'}).text.strip()

        if args:
            insult = u'{}: {}'.format(args[0], insult)

        return insult
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact Lutherean Insult API.' 

  def mormon(self, args, irc):
      cmnd = 'fortune -s -n {} mormon'.format(self.fortune_max_len)
      return sp.check_output(cmnd.split()).replace(u'\n', u' ')

  def north_korean_insult(self, args, irc):
    try:
        r = requests.get(self.NKI_URL)
        if r.status_code != 200:
            log.err('[Error]: Status code of {} for nki'.format(r.status_code))
            return
        
        soup = BeautifulSoup(r.text)
        insult = soup.find('div', id='insultContainer').text.strip()
        if args:
            insult = u'{}: {}'.format(args[0], insult)
        return insult
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact North Korean Insult API.' 

  def pickup(self, args, irc):
      '''(pickup [nick]) -- Random pickup line
      '''
      try:
          r = requests.get(self.PICKUP_LINES_URL)
          if not r.status_code == 200:
              return '[Error]: Invalid response from pickuplinegen.com.'

          soup = BeautifulSoup(r.text)
          line = soup.find_all('div', id='content')[0].text.strip()
          if args:
              line = u'{}: {}'.format(args[0], line)
          return line 
      except:
          log.err('[Error]: {}'.format(sys.exc_info()[0]))
          return '[Error]: Cannot contact Pickup Lines API.'


  def quran(self, args, irc):
    '''Random Quran quote
    '''
    try:
      r = requests.get(self.QURAN_URL)
      if not r.status_code == 200:
        return '[Error]: Invalid response from Quran API.' 

      soup = BeautifulSoup(r.text)
      quote = soup.find_all('h2')[-1].text
      passage = soup.find_all('p')[-2].text.strip().split()[-1]

      return u'{} {}'.format(passage, quote)
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact Quran API.'

  def shakespeare_insult(self, args, irc):
    '''(si [nick]) -- Random Shakespearian insult
    '''
    try:
        r = requests.get(self.SI_URL)
        if r.status_code != 200:
            log.err('[Error]: Status code of {} for si'.format(r.status_code))
            return
        
        soup = BeautifulSoup(r.text)
        insult = soup.find('p').text.strip()
        if args:
            insult = u'{}: {}'.format(args[0], insult)
        return insult
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return '[Error]: Cannot contact Shakespeare Insult API.' 

  def stab(self, args, irc):
    '''(stab [nicknames]) -- Stab peoples.  For Ex0deus.
    '''
    if not args:
        to_stab = irc.sender
    else:
        if len(args) == 1:
            to_stab = args[0]
        else:
            args[-1] = u'and {}'.format(args[-1])
            to_stab = u', '.join(args)

    action = u'stabs {} with a {} {} in the {}'.format( to_stab,
                random.choice(self.adj_list), random.choice(self.stab_list),
                random.choice(self.body_list))

    return u'\x01ACTION {}\x01'.format(action)

  def tao(self, args, irc):
    '''Random Tao quote.
    '''
    cmnd = 'fortune -s -n {} tao'.format(self.fortune_max_len * 2)
    return sp.check_output(cmnd.split()).replace(u'\n', u' ')

  def trolldb(self, args, irc):
    '''Get trolled.  Courtesy of Jason.
    '''
    if self.trolldb_max_len > 0:
        cmnd = 'fortune -s -n {} trolldb'.format(int(self.trolldb_max_len * 1.5))
    else
        cmnd = 'fortune trolldb'
    return sp.check_output(cmnd.split()).replace(u'\n', u'')
