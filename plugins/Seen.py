# -*- coding: utf-8 -*-

import cPickle as pickle
from datetime import datetime

from dateutil.relativedelta import relativedelta 

import plugins.PluginBase as pb

class Seen(pb.LinePlugin, pb.CommandPlugin):
  def __init__(self, conf):
    super(Seen, self).__init__(conf)

  def commands(self):
    return { 'seen': self.seen
           }

  def hasResponse(self, msg, irc):
    '''Hooks this method to save when a user
    was last seen.
    '''
    if not hasattr(irc, '_seend'):
      irc._seend = {}

    # Don't save info for PMs
    if irc.sender == irc.channel:
      return False

    if irc.channel in irc._seend:
      irc._seend[irc.channel][irc.sender] = (datetime.utcnow(), msg)
    else:
      irc._seend[irc.channel] = {irc.sender: (datetime.utcnow(), msg)}

  def loadSeenDict(self):
    '''Load the pickled seend from the
    bot's last run.
    '''

  def seen(self, args, irc):
    '''(seen [channel] <nick>) -- Returns
    the last time <nick> was seen in a given
    channel. [channel] is only required when
    the command is used in a PM. All times in UTC.
    '''
    if not args or (len(args) == 1 and irc.pm):
      return u'[Error]: seen [channel] <nick>'

    if len(args) == 2:
      channel, nick = args[0], args[1]
    else:
      channel, nick = irc.channel, args[0]

    if not hasattr(irc, '_seend'):
      irc._seend = {}
 
    if not channel in irc.channels:
      return u'I am not in {}'.format(channel)

    if not channel in irc._seend \
        or not nick in irc._seend[channel]:
          return u'I have not seen {} in {}'.format(nick, channel)

    dt, msg = irc._seend[channel][nick]
    rd = relativedelta(datetime.utcnow(), dt)

    # Build the time string
    time = []
    for attr in ('years', 'months', 'days', 'hours', 'minutes', 'seconds'):
        if getattr(rd, attr) != 0:
            time.append('{} {}'.format(getattr(rd, attr), attr))
    time = '{} ago'.format(u' '.join(time) if time else u'0 seconds')
    
    reply = u'{nick} was last seen in {chan} {time}: <{nick}> {msg}'.\
        format(nick=nick, chan=channel, time=time, msg=msg)
    return reply


