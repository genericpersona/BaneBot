# -*- coding: utf-8 -*-

import argparse
import datetime
import json 

import requests
from twisted.python import log

import plugins.PluginBase as pb
import utils.url as uurl
import utils.bitcoin as btc

class Bitcoin(pb.CommandPlugin):
  def __init__(self, conf):
    super(Bitcoin, self).__init__(conf)

    # BitcoinAverage attributes
    self.baa = btc.BitcoinAverageAPI()
    self.build_avg_parser()
    self.last_avg_fetch = None

    # Preev attributes
    self.build_preev_parser()
    self.preev_help()

  def commands(self):
    return { 'avg': self.avg
           , 'balance': self.balance
           , 'preev': self.preev
           }

  def avg(self, args, irc):
    '''(avg [--ask] [--bid] [-d/--day-avg] [--last] [-v/--verbose]
    [--volume-btc] [--volume-percent]) --
    Return the average price of BTC in USD from bitcoinaverage.com
    '''
    if self.avg_data_stale():
        if not self.get_fresh_avg_data():
            irc.pm = True
            return '[Error]: Failed to contact BitcoinAverage API'
        
    try:
        opts = self.avg_parser.parse_args(args)
        opts.currency = opts.currency.upper()
    except ArgParserError, exc:
        irc.pm = True
        return str(exc)

    if opts.currency not in self.baa.all:
        return u'[Error]: {} is not a supported currency'.format(opts.currency)

    if opts.verbose:
        reply = []
        for k, v in self.baa.all[opts.currency].iteritems():
            if k == 'timestamp':
                continue
            reply.append(u'{}: {}'.format(k.replace(u'_', u' ').title(), v))
        return u', '.join(reply)

    reply = []
    for stat in (u'ask', u'bid', u'day_avg', u'last', u'volume_btc', u'volume_percent'):
        stat = u'24h_avg' if stat == u'day_avg' else stat
        if getattr(opts, stat):
            if stat in self.baa.all[opts.currency]:
                reply.append(u'{}: {}'.format(stat.replace(u'_', u' ').title(), 
                             self.baa.all[opts.currency][stat])) 
            else:
                reply.append(u'{}: Not available.'.format(stat.replace(u'_', u' ').title()))

    if not reply:
        return unicode(self.baa.all[opts.currency]['last'])

    if len(reply) == 1:
        return reply[0].split(':')[-1].lstrip()

    return u', '.join(reply)

  def avg_data_stale(self):
    '''Check if new average data needs to be fetched.
    '''
    if self.last_avg_fetch is None:
        return True

    return (datetime.datetime.utcnow() - self.last_avg_fetch).seconds > self.avg_refresh_rate

  def balance(self, args, irc):
    '''(balance [address]) --
    Return the balance of a given Bitcoin address. Defaults to 6 confirms
    before an input is accepted. Pass a number after the address to change this.
    balance address [min confirms (default: 6)]'
    '''
    if len(args) < 1:
      return '{}balance address [min confirms (default: 6)]'
    else:
      addr = args[0]
      if not btc.valid_address(addr):
        return '{} is not a valid Bitcoin address'.format(addr)

      if len(args) > 1:
        try:
          min_confirms = int(args[1]) if int(args[1]) >= 0 else 6
          return str(btc.balance(addr, min_confirms))
        except:
          pass

      return str(btc.balance(addr))

  def build_avg_parser(self):
    '''Build a parser for the avg command.
    '''
    # Build an argument parser
    self.avg_parser = ArgParser( description='Call the BitcoinAverage API'
                               , add_help=False
                               )

    self.avg_parser.add_argument( '--ask'
                                , action='store_true'
                                , help='Ask price'
                                )
    self.avg_parser.add_argument( '--bid'
                                , action='store_true'
                                , help='Ask price'
                                )
    self.avg_parser.add_argument( '-d'
                                , '--day-avg'
                                , action='store_true'
                                , dest='24h_avg'
                                , help='Get 24 hour avg if available'
                                )
    self.avg_parser.add_argument( '--last'
                                , action='store_true'
                                , help='Get the last from the ticker'
                                )
    self.avg_parser.add_argument( '-v'
                                , '--verbose'
                                , action='store_true'
                                , help='Print all data for a given currency'
                                )
    self.avg_parser.add_argument( '--volume-btc'
                                , action='store_true'
                                , help='Volume in BTC'
                                )
    self.avg_parser.add_argument( '--volume-percent'
                                , action='store_true'
                                , help='Volume percentage'
                                )

    # Required, but w/ a default
    self.avg_parser.add_argument( 'currency'
                                , default=self.default_currency
                                , nargs='?'
                                , help='Get the avg price'
                                )
    return self.avg_parser

  def build_preev_parser(self):
    '''Build a parser for the avg command.
    '''
    # Build an argument parser
    self.preev_parser = ArgParser( description='Get the Preev ticker'
                                 , add_help=False
                                 )

    self.preev_parser.add_argument( '-x'
                                  , '--without'
                                  , choices=self.preev_exchanges('ALL')
                                  , default=[]
                                  , nargs='*'
                                  , help='List of space separated exchanges NOT to include' 
                                  )
    self.preev_parser.add_argument( '-c'
                                  , '--coin'
                                  , choices=[u'BTC', u'LTC', u'PPC', u'XDG']
                                  , default=self.default_coin.upper()
                                  , nargs='?'
                                  , help='Which coin to get the ticker for' 
                                  )

    # Required, but w/ a default
    self.preev_parser.add_argument( 'currency'
                                  , choices=[u'USD', u'EUR', u'GBP', u'CAD', u'AUD', \
                                             u'XAU', u'XAG', u'XPT', u'XPD']
                                  , default=self.default_currency.upper()
                                  , nargs='?'
                                  , help='Get the avg price'
                                  )
    return self.preev_parser

  def get_fresh_avg_data(self):
      '''Get up-to-date average data.
      '''
      self.last_avg_fetch = datetime.datetime.utcnow()
      return self.baa.saveAll()

  def preev(self, args, irc):
      '''(preev [-x/--without exchanges] [-c/--coin coin] [currencies])
      Return a ticker as quoted on preev.com.
      Defaults to BTC in USD. Visit preev.com for supported coins and
      currencies. Use -x to exclde certain exchanges from the rate.
      '''
      try:
          opts = self.preev_parser.parse_args(args)
      except ArgParserError, exc:
          irc.pm = True
          return str(exc)

      exchanges = [xchg for xchg in self.preev_exchanges(opts.coin) \
                  if xchg not in opts.without]
      return self.preev_ticker(opts.currency, opts.coin, exchanges)

  def preev_bases(self):
      '''Returns base currencies returned by preev.
      '''
      return (u'USD', u'EUR')

  def preev_exchanges(self, coin):
      '''Return all possible preev exchanges for a given coin.
      '''
      exchanges = { u'BTC': [u'bitfinex', u'bitstamp', u'btce', u'localbitcoins'] 
                  , u'LTC': [u'btce']
                  , u'XDG': [u'bter', u'cryptsy']
                  }
      exchanges[u'PPC'] = exchanges[u'LTC']
      for metal in self.preev_metals():
          exchanges[metal] = exchanges[u'BTC']

      if coin.upper() == 'ALL':
          return set([x for xchgs in exchanges.values() for x in xchgs])
      
      return exchanges[coin.upper()]

  def preev_help(self):
      self._helpd[u'preev'] = self.preev_parser.format_usage()

  def preev_metals(self):
      return (u'XAU', u'XAG', u'XPT', u'XPD')

  def preev_ticker(self, currency, coin, exchanges):
      '''Return the value quoted on the preev.com for a given currency and list 
      of exchanges.
      '''
      PREEV_URL = u'http://preev.com/pulse/units:{}+{}/sources:{}'
      PREEV_URL = PREEV_URL.format(coin.lower(), currency.lower(), u'+'.join(exchanges))
      log.msg(PREEV_URL)
      preev = uurl.safe_get([PREEV_URL], None)
      if preev is not None:
          preev_dict = json.loads(preev)

          # Special handling of metals
          if currency.upper() not in self.preev_bases():
              div_price = preev_dict[currency.lower()]['usd']['other']['last']
              if div_price is None:
                  return u'Ticker for {} per {} not available'.format(currency, coin)
              currency = u'usd'
          else:
              div_price = 1.0

          last_vols = []
          total_vol = 0.0
          for inner in preev_dict[coin.lower()][currency.lower()].values():
              last_vols.append((float(inner['last']), float(inner['volume'])))
              total_vol += last_vols[-1][-1]

          wavg = 0.0
          for last, vol in last_vols:
              wavg += last * (vol / total_vol)

          return str(round(wavg / div_price, 2))
      else:
          error = '[Error]: Unable to access preev ticker'
          log.err(error)
          return error
            

#-------------------------------------
#
#    Helper Classes and Functions
#
#-------------------------------------
class ArgParserError(Exception): pass

class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgParserError(message)

