# -*- coding: utf-8 -*-

import argparse
import datetime
import subprocess as sp
import sys
import urllib2

from bs4 import BeautifulSoup
import ipaddress as ip
from pygoogle import pygoogle   # https://code.google.com/p/pygoogle/
import pythonwhois as whois
import requests
from twisted.python import log
import wikipedia

from plugins.areacodes import areacodes
import plugins.PluginBase as pb

class Lookup(pb.CommandPlugin):
  DOJ_URL = 'http://doj.me/?url={}'
  OMDB_URL = 'http://www.omdbapi.com/?t={}&plot=short&r=json'
  WEATHER_URL = \
    'http://api.openweathermap.org/data/2.5/weather?q={}' + \
    '&cnt=1&mode=json&units=imperial'

  def __init__(self, conf):
    super(Lookup, self).__init__(conf)

    self.forex_api = ForexAPI(self.forex_api_key, self.forex_refresh_rate)
    self.geoip_api = GeoIPAPI()
    self.stock_api = StockAPI()
    self.ud_api = UrbanDictionaryAPI()

  def areacode(self, args, irc):
    '''Lookup a NANP area code.
    '''
    # Change the type of acodes
    acodes = [int(c) for c in args if \
                                  c.isdigit()]

    # Generate a reply to each of the codes
    replies = []
    for code in acodes:
      if code in areacodes:
        cities, state = areacodes[code][:-1], areacodes[code][-1]
        reply = u'[{}]: {}'.format(code, state if not cities \
            else state + u': ' + u', '.join(cities))
      else:
        reply = u'[{}]: Invalid NANP area code'.format(code)

      replies.append(reply)

    return u' | '.join(replies)

  def commands(self):
    return { 'areacode': self.areacode
           , 'dict': self.dictionary
           , 'dns': self.dns
           , 'forex': self.forex
           , 'geoip': self.geoip
           , 'gold': self.gold
           , 'google': self.google
           , 'isitdown': self.doj_me
           , 'isitup': self.doj_me
           , 'jukebox': self.jukebox
           , 'omdb': self.omdb
           , 'online': self.online
           , 'silver': self.silver
           , 'stock': self.stock
           , 'ud': self.ud
           , 'weather': self.weather
           , 'whois': self.whois
           , 'wikipedia': self.wikipedia
           , 'wp': self.wikipedia
           }

  def dictionary(self, args, irc):
    '''(dict [word or phrase]) -- Lookup up a word using WordNet.
    '''
    if not args:
        return u'Missing word or phrase to look up'

    try:
        cmnd = 'sdcv -u WordNet -n --utf8-input --utf8-output'.split() + args
        o = [line.strip() for line in sp.check_output(cmnd).split('\n') if line]

        if len(o) == 1:
            return o[0]
        else:
            return u' '.join(o[3:])
    except:
        log.error('[Error]: dict {}'.format(sys.exc_info()[0]))

  def dns(self, args, irc):
    '''(dns [hostname/IP address]) -- A or PTR record lookup.
    '''
    if not args:
        return u'Missing IP address or hostname'

    q = unicode(args[0])
    cmnd = u'dig +short '
    rev_cmnd = cmnd + u' -x '
    o = None
    try:
        ip.ip_address(q)
        o = sp.check_output((rev_cmnd + q).split())
    except ValueError:
        pass

    if o is None:
        o = sp.check_output((cmnd + q).split())
    answer = o.rstrip().replace(u'\n', u' | ')
    return answer if answer else u'No answers found.'

  def doj_me(self, args, irc):
    '''(isitdown [hostname]) -- Check if a given site is up or down according to doj.me.
    '''
    if not len(args):
        return u'{}{} [URL to check]'.format(irc.fact.prefix, irc.cmnd)

    try:
        r = requests.get(self.DOJ_URL.format(args[0]))
        if r.status_code != 200:
            log.err('[Error]: doj.me status code of {}'.format(r.status_code))
            return

        soup = BeautifulSoup(r.text)
        try:
            return soup.find('div', {'class': 'result'}).text
        except:
            log.err('[Error]: doj.me problem with soup')
    except:
        log.err('[Error]: doj.me {}'.format(sys.exc_info()[0]))

  def forex(self, args, irc):
    '''(forex [-a/--available] [-n/--long-name] [-s/--short-answer]
    [currencies]) -- Given a three letter currency code,
    look up forex data from openexchangerates.org, check if a given
    currency code is available or get the long name for a currency
    code.
    '''
    if self.forex_api.stale():
        if not self.forex_api.get_data():
            irc.pm = True
            return '[Error]: Cannot obtain fresh forex API data.'

    try:
        opts = self.forex_api.parser.parse_args(args)
        currencies = opts.currencies
    except ArgParserError, exc:
        irc.pm = True
        return str(exc)

    if opts.available:
        reply = []
        for ccode in opts.available:
            reply.append(u'{} is{} supported'.format(ccode,
                                                '' if ccode.upper() \
                                                    in self.forex_api.cs \
                                                      else ' NOT'))
            return u' | '.join(reply)

    if opts.long_name:
        reply = map( lambda x: u'[{}]: {}'.format(x, self.forex_api.cs[x]) \
                                                  if x in self.forex_api.cs
                                                  else ''
                   , opts.long_name
                   )
        return u' | '.join(x for x in reply if x)

    pairs = [(currencies[i], currencies[i+1]) \
                         for i in range(0, len(currencies), 2)]

    # Build the reply
    replies = []
    for pair in pairs:
      reply = ''
      cfrom, cto = pair

      error = False
      if not cfrom.upper() in self.forex_api.cs:
        reply = '[{}]: Invalid currency code '.format(cfrom)
        error = True

      if not cto.upper() in self.forex_api.cs:
        reply += '[{}]: Invalid currency code'.format(cto)
        error = True

      if error:
        replies.append(reply)
        continue

      if opts.short_answer:
          reply += '{}'.format(self.forex_api.get_rate(cfrom.upper(), cto.upper()))
      else:
          reply += '1 {cfrom} equals {rate} {cto}'.format(\
              cfrom=self.forex_api.long_name(cfrom),
              cto=self.forex_api.long_name(cto),
              rate=self.forex_api.get_rate(cfrom.upper(), cto.upper()))

      replies.append(reply)

    return u' | '.join(replies)

  def geoip(self, args, irc):
    '''(geoip [IPv4/IPv6 address]) -- 
    Perform a GeoIP lookup for a single IPv4 or IPv6 address.
    Returns information about city, region, country, ASN, and ISP.
    '''
    if not len(args):
      return '[Error]: {}geoip [IPv4/IPv6 address]'.format(irc.fact.prefix)

    return self.geoip_api.lookup(args[0].replace(u'-', u'.'))

  def gold(self, args, irc):
    return self.forex(['XAU', 'USD'], irc)

  def google(self, args, irc):
    '''(google [search term]) -- 
    Return the top Google result for the term searched.
    '''
    try:
        g = pygoogle(u' '.join(args))
        g.pages = 1
        for title, descr in g.search().iteritems():
            reply = u'{} | {}'.format(descr.strip(), title.strip())
            return reply
    except:
        log.err('[Error]: Google {}'.format(sys.exc_info()[0]))
        return '[Error]: Cannot contact Google API.'

  def jukebox(self, args, irc):
    '''(jukebox [song/artist]) --
    Return a Grooveshark link for a given search term. Command
    provided by Elio19.
    '''
    if not args:
        return 'Missing search term.'

    gs_url = u'http://grooveshark.com/#!/search?q={}'.format(u'+'.join(args))
    return gs_url

  def omdb(self, args, irc):
    '''(omdb [movie title]) --
    Return information about a movie title from the OMDb.
    '''
    if not args:
        return u'[Error]: Missing movie title'

    try:
        r = requests.get(self.OMDB_URL.format(u'+'.join(args)))

        if not r.status_code == 200:
            irc.pm = True
            return u'[Error]: Invalid status code from OMDb'

        rj = r.json()

        if rj['Response'] == u'False':
            return u'{} not found'.format(u' '.join(args))

        reply = []
        for key in (u'Title', u'Year', u'Rated', u'Director', u'Plot'):
            reply.append(u'{}: {}'.format(key, rj[key]))

        return u' | '.join(reply)

    except:
        irc.pm = True
        return u'[Error]: Cannot connect to OMDb API'

  def online(self, args, irc):
    '''(online [nick/user/hostname]) --
    Checks whether a user is on IRC using the WHO command.
    '''
    if not args:
        return u'[Error]: {}online <nickname>'.format(irc.fact.prefix)

    # Send the WHO command, which is handled in BaneBot
    irc.who_reply = (None, args[0])
    irc.sendLine('WHO {}'.format(args[0]))

  def silver(self, args, irc):
    return self.forex(['XAG', 'USD'], irc)

  def stock(self, args, irc):
    '''(stock [-i/--info company] [ticker]) -- 
        By default, lookup data about a given stock ticker.
        The -i/--info command allows querying about a company name
        to find its ticker information.
    '''
    if not args or (args[0] in (u'-i', u'--info') and len(args) == 1):
        return u'[Error]: Missing ticker or company name'

    if args[0] in (u'-i', u'--info'):
        return self.stock_api.lookup(u''.join(args[1:]))
    else:
        return self.stock_api.quote(args[0])

  def ud(self, args, irc):
    '''(ud [term/phrase]) -- 
    Return the definitions and examples for a term/phrase on Urban Dictionary
    '''
    if not len(args):
        return u'[Error]: {}ud [term/phrase]'.format(irc.fact.prefix)
    
    reply = self.ud_api.lookup_all(u''.join(args))
    return reply if reply else u'Nothing found for {}'.format(u' '.join(args))

  def weather(self, args, irc):
    '''(weather [place]) --
    Return weather data about a particular place.
    '''
    city = urllib2.quote(u' '.join(args))
    try:
      # Go get some weather
      r = requests.get(self.WEATHER_URL.format(city))

      if r.status_code != 200 or not 'main' in r.json():
        reply = 'No weather data found for {}'.format(\
                              urllib2.unquote(city).strip())
        return reply
      else:
        rjson = r.json()
        faren = rjson['main']['temp']
        cels = round(float(faren - 32) / 1.8, 2)

        reply = u'In {}, {}'.format(\
            urllib2.unquote(city).strip().title(), rjson['sys']['country'])
        reply += u' it is currently {}\u00b0F/{}\u00b0C'.format(faren, cels)
        log.msg(reply)

        descr = rjson['weather'][0]['description']
        if ' is ' in descr:
          reply += ' and the {}'.format(descr)
        else:
          reply += ' with {}'.format(descr)

        return reply
    except:
        log.err('[Error]: {}'.format(sys.exc_info()[0]))
        return '[Error]: Cannot contact Weather API.' 

  def whois(self, args, irc):
    '''(whois [domain]) --
    Return whois data for a given domain.
    '''
    if not args:
        return 'Missing domain for whois lookup'

    try:
        wd = whois.get_whois(args[0])
        replies = []
        for k in ('creation_date', 'expiration_date'):
            if k in wd:
                replies.append('{}: {}'.format(k.replace('_', ' ').title(),
                                               str(wd[k][0]).split()[0]))

        contact_dict = wd['contacts']['registrant']
        for k in ('name', 'city', 'state', 'country', 'email', 'phone'):
            if k in contact_dict:
                replies.append('{}: {}'.format(k.title(), contact_dict[k]))

        return u' | '.join(replies)
    except whois.shared.WhoisException:
        return 'Cannot find TLD for {}'.format(args[0])

  def wikipedia(self, args, irc):
      '''(wp [term]) -- 
      Lookup a term on Wikipedia and get summary information.
      '''
      try:
          if self.wp_sentences is not None:
              result = wikipedia.summary(u' '.join(args), 
                                sentences=self.wp_sentences)
          else:
              result = wikipedia.summary(u' '.join(args))

          return u' '.join(result.replace(u'\n', u' ').split())
      except wikipedia.exceptions.PageError:
          return u'No results found for {}'.format(u' '.join(args))
      except wikipedia.exceptions.DisambiguationError as de:
          return u'{} is too ambiguous. Try {}'.format(u' '.join(args),
                                                u' or '.join(de.options[:3]))
      except:
          log.err('[Error]: Wikipedia {}'.format(sys.exc_info()[0]))
          return '[Error]: Cannot contact Wikipedia API.'

#----------------------------------------
#
#           Lookup Classes
#
#----------------------------------------
class GeoIPAPI(object):
    GEOIP_URL = 'http://www.telize.com/geoip/{}'

    def __init__(self):
        pass

    def lookup(self, ip_addr):
        try:
            r = requests.get(self.GEOIP_URL.format(ip_addr))

            if r.status_code == 200:
                geoip_dict = r.json()
                reply = []
                for k in (u'IP', u'City', u'Region', u'Country', u'ASN', u'ISP'):
                    if k.lower() in geoip_dict and geoip_dict[k.lower()]:
                        info = u'[{}]: {}'.format(k, geoip_dict[k.lower()])
                        reply.append(info)
                return u' | '.join(reply)
            elif r.status_code == 400:
                return '[Error]: Invalid IP address.'
            else:
                return '[Error]: Invalid status code from GeoIP API.'
        except:
            log.err('[Error]: {}'.format(sys.exc_info()[0]))
            return '[Error]: Cannot contact GeoIP API.'

class ForexAPI(object):
    FOREX_LATEST = 'http://openexchangerates.org/api/latest.json?app_id={}'
    FOREX_CS = 'http://openexchangerates.org/api/currencies.json?app_id={}'
    FOREX_BASE = 'USD'
    def __init__(self, api_key, refresh_rate):
        self.forex_latest = self.FOREX_LATEST.format(api_key)
        self.forex_cs_url = self.FOREX_CS.format(api_key)
        self.refresh_rate = refresh_rate

        self.last_get = None
        self.cs = {} # List/dict of forex currencies
        self.build_parser()

    def build_parser(self):
        self.parser = ArgParser( description='Retrieve forex data'
                               , add_help=False
                               )

        self.parser.add_argument( '-a'
                                , '--available'
                                , nargs='+'
                                , help='Find out if particular currencies are supported'
                                )
        self.parser.add_argument( '-n'
                                , '--long-name'
                                , nargs='*'
                                , help='Find out the long name of a currency code'
                                )
        self.parser.add_argument( '-s'
                                , '--short-answer'
                                , action='store_true'
                                , help='Return the rate without any additional text'
                                )
        self.parser.add_argument( 'currencies'
                                , nargs='*'
                                , help='Currencies to find the rate of'
                                , action=EvenAndMinMaxPairs
                                )

    def get_data(self):
        try:
            r = requests.get(self.forex_latest)

            for k, v in r.json().iteritems():
                setattr(self, 'forex_' + k, v)

            if not self.cs:
                r = requests.get(self.forex_cs_url)
                self.cs = r.json()

            self.last_get = datetime.datetime.utcnow()
            return True
        except:
            log.err('[Error]: Forex {}'.format(sys.exc_info()[0]))
            return False

    def get_rate(self, cfrom, cto):
        if cto == self.FOREX_BASE:
            return round(float(1 / self.forex_rates[cfrom]), 2)
        elif cfrom == self.FOREX_BASE:
            return round(float(self.forex_rates[cto]), 2)

        from_frac = float(1 / self.forex_rates[cfrom])
        to_frac = float(self.forex_rates[cto])
        return round(from_frac * to_frac, 2)

    def long_name(self, cur):
        '''Return long name of a currency code, or
        the cur argument if not supported.
        '''
        return self.cs.get(cur, cur)

    def stale(self):
        if self.last_get is None:
            return True

        return (datetime.datetime.utcnow() - self.last_get).seconds > self.refresh_rate

class StockAPI(object):
    LOOKUP = 'http://dev.markitondemand.com/Api/v2/Lookup/json?input={}'
    QUOTE = 'http://dev.markitondemand.com/Api/v2/Quote/json?symbol={}'

    def __init__(self):
        pass

    def lookup(self, input_str):
        '''Lookup the ticker info for a company.
        '''
        try:        
            r = requests.get(self.LOOKUP.format(input_str))

            if r.status_code != 200:
                return u'No data returned for {}'.format(input_str)

            rj = r.json()
            if not rj:
                return u'No data returned for {}'.format(input_str)

            reply = map(lambda x: u'Symbol: {}, Name: {}, Exchange: {}'.\
                            format(x[u'Symbol'], x[u'Name'], x[u'Exchange']),
                        rj)
            return u' | '.join(reply)
        except:
            return u'[Error]: Cannot contact stock lookup API'

    def quote(self, symbol):
        '''Get a quote for a given stock symbol.
        '''
        try:        
            r = requests.get(self.QUOTE.format(symbol))

            if r.status_code != 200:
                return u'No data returned for {}'.format(input_str)

            rj = r.json()
            if not rj:
                return u'No data returned for {}'.format(input_str)

            reply = []
            for k in (u'Symbol', u'Name', u'Last Price', u'High', u'Low'):
                if k.replace(u' ', u'') in rj:
                    reply.append(u'{}: {}'.format(k, rj[k.replace(u' ', u'')]))

            if reply:
                return u' | '.join(reply)
            else:
                return rj[u'Message']

        except:
            return u'[Error]: Cannot contact stock lookup API'

class UrbanDictionaryAPI(object):
    UD_URL = 'http://api.urbandictionary.com/v0/define?term={}'

    def __init__(self, max_def_len=None, max_ex_len=None):
        self.max_def_len = max_def_len if max_def_len is not None else -1
        self.max_ex_len = max_ex_len if max_ex_len is not None else -1

    def lookup_all(self, term):
        '''Obtain all definitions on the first page of a term's results.
        '''
        try:
            r = requests.get(self.UD_URL.format(term.replace(u' ', u'+')))

            if r.status_code != 200:
                return u'No definitions found for: {}'.format(term)

            rjson = r.json()

            if rjson['result_type'] == 'no_results':
                return u'No definitions found for: {}'.format(term)

            reply = map( lambda x: u'{}. {} "{}"'.\
                         format( x['word'].title()
                               , x['definition'][:self.max_def_len]
                               , x['example'][:self.max_ex_len]
                               )
                       , rjson['list']
                       )

            return u' | '.join(reply)

        except:
            log.err('[Error]: UD Lookup {}'.format(sys.exc_info()[0]))
            return u'[Error]: Cannot contact Urban Dictionary API.'

class UrbanDictionaryAPI2(object):
    UD_URL = 'http://urbanscraper.herokuapp.com/define/{}'
    UD_SEARCH = 'http://urbanscraper.herokuapp.com/search/{}'

    def __init__(self, max_def_len=None, max_ex_len=None):
        self.max_def_len = max_def_len if max_def_len is not None else -1
        self.max_ex_len = max_ex_len if max_ex_len is not None else -1

    def lookup_first(self, term):
        '''Obtain the first definition for a word or phrase on Urban Dictionary.
        '''
        try:
            r = requests.get(self.UD_URL.format(term.replace(u' ', u'')))

            if r.status_code != 200:
                return u'No definitions found for: {}'.format(term)

            rjson = r.json()
            reply = u'{}. {} "{}"'.format( term.upper()
                                         , rjson['definition'][:self.max_def_len]
                                         , rjson['example'][:self.max_ex_len]
                                         )
            return reply

        except:
            log.err('[Error]: UD Lookup {}'.format(sys.exc_info()[0]))
            return u'[Error]: Cannot contact Urban Dictionary API.'

    def lookup_all(self, term):
        '''Obtain all definitions on the first page of a term's results.
        '''
        try:
            r = requests.get(self.UD_SEARCH.format(term.replace(u' ', u'')))

            if r.status_code != 200:
                return u'No definitions found for: {}'.format(term)

            rjson = r.json()
            reply = map( lambda x: u'{}. {} "{}"'.\
                         format( term.title()
                               , x['definition'][:self.max_def_len]
                               , x['example'][:self.max_ex_len]
                               )
                       , rjson
                       )

            # Get rid of replies with blank definitions and examples
            reply = [r for r in reply if u'  ""' not in r]

            return u' | '.join(reply)

        except:
            log.err('[Error]: UD Lookup {}'.format(sys.exc_info()[0]))
            return u'[Error]: Cannot contact Urban Dictionary API.'


#-------------------------------------
#
#    Helper Classes and Functions
#
#-------------------------------------
class ArgParserError(Exception): pass

class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgParserError(message)

class EvenAndMinMaxPairs(argparse.Action):
  min_pairs = 1
  max_pairs = 3
  def __call__(self, parser, args, values, option_string=None):
    def even(num):
      return num % 2 == 0

    # Get the number of values and pairs
    num_values = len(values)
    num_pairs = num_values / 2

    # Don't do tests if availabe argument selected
    if args.available or args.long_name:
      pass
    elif not even(num_values):
      msg = 'Must supply an even number of currencies to get rates ' + \
            'of, as the rate is of one currency relative to another'
      parser.error(msg)
    elif num_pairs < self.min_pairs or num_pairs > self.max_pairs:
      msg = 'Can only specify between {} and {} pairs, inclusive'.\
                      format(self.min_pairs, self.max_pairs)
      parser.error(msg)

    setattr(args, self.dest, values)
