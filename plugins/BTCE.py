# -*- coding: utf-8 -*-

import argparse
import datetime
import itertools
import sys

import requests
from twisted.python import log

import plugins.PluginBase as pb

class BTCE(pb.CommandPlugin):
  def __init__(self, conf):
    super(BTCE, self).__init__(conf)

    # Cache the time of the last
    # update so no more than a
    # given number of API calls
    # occur in a particular time
    self.last_update = None

    # Build a parser
    self.build_parser()

    # Initialize containers for API data
    self.currencies = set()

    # Get fresh data
    self.get_fresh_data()

  def build_parser(self):
    '''
    Builds a parser for the program.

    Return None.
    '''
    # Build an argument parser
    self.parser = ArgParser( description='Calculate the rate of two currencies on BTC-E'
                           , add_help=False
                           )

    self.parser.add_argument( '-a'
                            , '--available'
                            , nargs='+'
                            , help='Find out if particular coin(s) are available'
                            )
    self.parser.add_argument( '--avg'
                            , action='store_true'
                            , help='Get the avg price'
                            )
    self.parser.add_argument( '--buy'
                            , action='store_true'
                            , help='Get the buy price'
                            )
    self.parser.add_argument( '--high'
                            , action='store_true'
                            , help='Get the high from the ticker'
                            )
    self.parser.add_argument( '--last'
                            , action='store_true'
                            , help='Get the last from the ticker'
                            )
    self.parser.add_argument( '--low'
                            , action='store_true'
                            , help='Get the low from the ticker'
                            )
    self.parser.add_argument( '--sell'
                            , action='store_true'
                            , help='Get the sell price from the ticker'
                            )
    self.parser.add_argument( '--short'
                            , action='store_true'
                            , help='Short answer with minimal text'
                            )
    self.parser.add_argument( '-v'
                            , '--verbose'
                            , action='store_true'
                            , help='Get full ticker information'
                            )
    self.parser.add_argument( 'currencies'
                            , help='Currencies to find the rate of'
                            , nargs='*'
                            , action=EvenAndMinMaxPairs
                            )

  def commands(self):
    return { 'btc-e': self.ticker
           }

  def get_fresh_data(self):
    '''
    Grab fresh data from the API and saves
    it in class attributes.

    Returns True if grab was successful
    and False if an error occurred.
    '''
    try:
      # Now, grab the pairs data
      r = requests.get(self.info_api)
      if r.status_code != 200:
        log.err('[Error]: Status code {} for listing coins'.\
                    format(r.status_code))
        return False
      else:
        self.currencies = set()

        # Save all the currencies 
        for k in r.json()['pairs']:
            left, right = k.split(u'_')
            self.currencies.add(left)
            self.currencies.add(right)

        # Save the timestamp
        self.last_update = datetime.datetime.utcnow() 

        return True
    # Any error that occurs connecting to the API
    except:
      log.err('[Error]: Cannot get fresh BTC-E data')
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return False

  def stale(self):
    '''
    Return True if API data is stale.
    '''
    # See if a pull from the API
    # has never been made
    if not self.last_update:
      return True

    return (datetime.datetime.utcnow() - self.last_update).seconds > self.refresh_rate

  def ticker(self, args, irc):
    '''(btc-e [-a/--available] [--avg] [--buy] [--high] [--last] [--low] 
    [--sell] [--short] [-v/--verbose] [currencies]) -- 
    Obtain information from BTC-E's ticker, or use -a/--available to check if a
    currency is available.  All other options control what info is returned.
    '''
    # Get fresh data if needed
    if self.stale():
      if not self.get_fresh_data():
        log.err('Failed to obtain fresh API average data')
        irc.pm = True
        return '[Error]: Cannot access BTC-E API.'

    # Parse the command
    try:
      # Allow for a default currency
      if len(args) == 1 or \
          (len(args) == 2 and \
          '-v' in args or '--verbose' in args):
        args.append(self.default_currency)

      # Parse the command
      args = self.parser.parse_args(args)
      currencies = args.currencies
    except ArgParserError, exc:
      irc.pm = True
      return str(exc)

    # Check if we're checking for coin support
    if args.available:
      reply = []
      for coin in args.available:
        reply.append(u'{} is{} supported'.format(coin,
                                          u'' if self.supported(coin) \
                                             else u' NOT'))

      return u' | '.join(reply)

    # Get the pairs in a useable format
    pairs = [(currencies[i], currencies[i+1]) for i in range(0, len(currencies), 2)]
    payload = u'-'.join(map(lambda x: u'{}_{}'.format(x[0], x[1]), pairs))

    # Set up data for a request
    try:
      r = requests.get(self.ticker_api.format(payload))

      # Check for valid status code
      if r.status_code != 200:
        log.err('[Error]: Status code {} for BTC-E API'.format(r.status_code))
        irc.pm = True
        return '[Error]: Cannot contact BTC-E API.'

      # Get all returned pair(s)
      ret_pairs = r.json()

      # Build the reply
      replies = []
      for pair, data in ret_pairs.iteritems():
          if args.short:
            reply = u''
          else:
            reply = u'{} Ticker | '.format(pair.replace(u'_', u'/').upper())
          stats = []
          for stat in (u'high', u'low', u'avg', u'vol', u'last', u'buy', u'sell'):
              if (hasattr(args, stat) and getattr(args, stat)) or args.verbose:
                  if args.short:
                    stats.append(u'{}'.format(data[stat]))
                  else:
                    stats.append(u'{}: {}'.format(stat.title(), data[stat]))
        
          # Default to the average
          if not stats:
              if args.short:
                  stats.append(u'{}'.format(data[u'avg']))
              else:
                stats.append(u'Avg: {}'.format(data[u'avg']))

          replies.append(reply + u', '.join(stats))

      return u'\n'.join(replies)
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      irc.pm = True
      return '[Error]: Cannot contact BTC-E API.'


  def supported(self, curr):
    '''
    Tests if the passed in code is supported in the
    CryptoCoin API.

    Can toggle whether currencies are included in the
    check.

    Return True if supported and False otherwise.
    '''
    return curr.lower() in self.currencies

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
    if args.available: 
      pass
    elif not even(num_values):
      msg = 'Must supply an even number of currencies to get rates ' + \
            'of, as the rate is of one currency relative to another'
      parser.error(msg)
    elif num_pairs < self.min_pairs or num_pairs > self.max_pairs:
      if self.min_pairs < self.max_pairs:
          msg = 'Can only specify between {} and {} pairs, inclusive, '.\
                          format(self.min_pairs, self.max_pairs)
      else:
          msg = 'Can only specify {} pair{}'.format(self.min_pairs, 's' if self.min_pairs > 1 else '')
      parser.error(msg)

    setattr(args, self.dest, values)
