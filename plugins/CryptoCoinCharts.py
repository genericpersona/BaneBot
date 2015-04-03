# -*- coding: utf-8 -*-

import argparse
from csv import DictReader
import datetime
import itertools
from operator import itemgetter
import sys

import requests
from twisted.python import log

import plugins.PluginBase as pb

class CryptoCoinCharts(pb.CommandPlugin):
  def __init__(self, conf):
    super(CryptoCoinCharts, self).__init__(conf)

    # Cache the time of the last
    # update so no more than a
    # given number of API calls
    # occur in a particular time
    self.last_update = None

    # Build a parser
    self.build_parser()

    # Initialize containers for API data
    self.coins = {}
    self.pairs = {}

    # Get fresh data
    self.get_fresh_data()

    # Get a list of currencies
    self.get_currencies()

  def build_parser(self):
    '''
    Builds a parser for the program.

    Return None.
    '''
    # Build an argument parser
    self.parser = ArgParser( description='Calculate the rate of two coins on CryptoCoinCharts'
                           , add_help=False
                           )

    self.parser.add_argument( '-a'
                            , '--available'
                            , nargs='+'
                            , help='Find out if particular coin(s) are available'
                            )
    self.parser.add_argument( '-n'
                            , '--long-name'
                            , dest='long_name'
                            , nargs='*'
                            , help='Get long name for currency codes or coins'
                            )
    self.parser.add_argument( '-s'
                            , '--short-answer'
                            , action='store_true'
                            , help='Return numbers without prose'
                            )
    self.parser.add_argument( '-v'
                            , '--verbose'
                            , action='store_true'
                            , help='Get additional information on rates'
                            )
    self.parser.add_argument( 'currencies'
                            , help='Currencies to find the rate of'
                            , nargs='*'
                            , action=EvenAndMinMaxPairs
                            )

  def commands(self):
    return { 'ccc': self.rate
           , 'cryptocoins': self.rate
           }

  def get_currencies(self):
    '''
    Obtain a list of currencies
    used for calculating rates of
    various CryptoCoins. Store this
    list
    '''
    if not hasattr(self, 'currencies'):
      with open(self.currencies_csv) as csvf:
        # Create a reader object and save the dicts
        reader = DictReader(csvf)

        # Save the dictionaries
        reader = [cd for cd in reader]

        # Save the currencies as a set
        self.currencies = sorted(set(map(itemgetter('AlphabeticCode'),
                                                            reader)))
        self.currencies = [c for c in self.currencies if c.strip()]

        # Also, save mapping of currencies
        # to a longer name for them
        self.name_currencies = {d['AlphabeticCode']: d['Currency'] \
                                for d in reader \
                                  if d['AlphabeticCode'] in \
                                      self.currencies}

    return self.currencies

  def get_fresh_data(self):
    '''
    Grab fresh data from the API and saves
    it in class attributes.

    Returns True if grab was successful
    and False if an error occurred.
    '''
    try:
      # Now, grab the pairs data
      r = requests.get(self.api_list_coins, timeout=5)
      if r.status_code != 200:
        log.err('[Error]: Status code {} for listing coins'.\
                    format(r.status_code))
        return False
      else:
        self.coins = {}
        for coind in r.json():
          # Don't take any coins with zero volume
          if not float(coind['volume_btc']):
            continue
          # Otherwise, save the information
          self.coins[coind['id']] = {k: v for k,v in coind.iteritems() \
                                                  if k != 'id'}

        # Also save a list of coin names
        self.names = {str(x.upper()) for x in self.coins.iterkeys()}

        # Finally, get some currencies
        self.get_currencies()

        # Save the timestamp
        self.last_update = datetime.datetime.utcnow() 

        return True
    # Any error that occurs connecting to the API
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      return False

  def rate(self, args, irc):
    '''(ccc [-a/--available] [-n/--long-name] [-s/--short-answer]
    [-v/--verbose] [currencies]) --
    Obtain information from CryptoCoinCharts.
    '''
    # Get fresh data if needed
    if self.stale():
      if not self.get_fresh_data():
        log.err('Failed to obtain fresh API average data')
        irc.pm = True
        return '[Error]: Cannot access CryptoCoinCharts API.'

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

    # Check for long name checking
    if args.long_name:
      reply = map( lambda x: u'[{}]: '.format(x.upper()) + \
                             self.coins[x.lower()]['name'] \
                             if x.lower() in self.coins
                             else self.name_currencies[x.upper()] \
                                  if x.upper() in self.currencies
                                  else u''
                 , args.long_name
                 )
      return u' | '.join(x for x in reply if x)

    # Get the pairs in a useable format
    pairs = [(currencies[i], currencies[i+1]) for i in range(0, len(currencies), 2)]
    payload = u','.join(map(lambda x: u'{}_{}'.format(x[0], x[1]), pairs))

    # Figure out if you need to use pair or pairs
    if len(pairs) > 1:
      post = irc.pm = True
    else:
      post = False

    # Make sure all the pairs are supported
    if not all(map(self.supported, currencies)):
      reply = '[Error]: Invalid coin specified.'
      reply += ' | Use the -c/--coins option to see all supported'
      return reply

    # Set up data for a request
    try:
      # Make the proper request
      if post:
        r = requests.post(self.api_pairs, data=payload)
      else:
        r = requests.get('{}{}'.format(self.api_pair, payload))

      # Check for valid status code
      if r.status_code != 200:
        log.err('[Error]: Status code {} for pairs API'.format(r.status_code))
        irc.pm = True
        return '[Error]: Cannot contact CryptoCoinCharts API.'

      # Get all returned pair(s)
      ret_pairs = r.json if type(r.json) == list else [r.json()]

      # Build the reply
      replies = []
      for i, pair in enumerate(ret_pairs):
        if pair['id'] is None:
          reply = '[Error]: No response for {}. Try {}'.\
              format( u' '.join(pairs[i])
                    , u'{} {}'.format(pairs[i][-1].upper(), pairs[i][0].upper())
                    )
        else:
          if args.short_answer:
              reply = u'{}'.format(round(float(pair['price']), 8))
          else:
              reply = u'{pair}{price}{convert}{v}'.\
                  format( pair=u'[{}]: '.format(pair['id'].upper())
                        , price=round(float(pair['price']), 8)
                        , convert=u' | {} {} for 1 {}'.\
                            format( round(1.0 / float(pair['price']), 8)
                                  , pairs[i][0].upper()
                                  , pairs[i][1].upper()
                                  ) if not (pairs[i][0] in self.currencies or \
                                            pairs[i][1] in self.currencies) \
                                    else ''
                        , v=u' | [Best Market]: {}'.format(pair['best_market']) \
                                if args.verbose else u''
                        )
        replies.append(reply)

      return u' | '.join(replies)
    except:
      log.err('[Error]: {}'.format(sys.exc_info()[0]))
      irc.pm = True
      return '[Error]: Cannot contact pairs API.'

  def stale(self):
    '''
    Return True if API data is stale.
    '''
    # See if a pull from the API
    # has never been made
    if not self.last_update:
      return True

    return (datetime.datetime.utcnow() - self.last_update).seconds > 60

  def supported(self, code, include_currencies=True):
    '''
    Tests if the passed in code is supported in the
    CryptoCoin API.

    Can toggle whether currencies are included in the
    check.

    Return True if supported and False otherwise.
    '''
    if include_currencies:
      return code.upper() in self.names or code.upper() in self.currencies
    else:
      return code.upper() in self.names

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
  max_pairs = 5
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
