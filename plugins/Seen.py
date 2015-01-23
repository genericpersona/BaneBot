# -*- coding: utf-8 -*-

import cPickle as pickle
from datetime import datetime
import os
import zlib

from dateutil.relativedelta import relativedelta 

import plugins.PluginBase as pb

class Seen(pb.LinePlugin, pb.CommandPlugin):
  def __init__(self, conf):
    super(Seen, self).__init__(conf)

  def commands(self):
    return { 'seen': self.seen
           }
 
  def deleteOldestN(self, n, irc):
    '''Delete the oldest n seen messages.
    '''
    if not hasattr(irc, '_seend'):
        return

    entries = []
    for chan in irc._seend:
        for nick in irc._seend[chan]:
            entries.append((chan, nick, irc._seend[chan][nick][0]))

    entries_sorted = sorted(entries, key=lambda x: x[-1])
    for i, entry in enumerate(entries_sorted):
        if i >= n: 
            break

        chan, nick, _ = entry
        del irc._seend[chan][nick]

  def hasResponse(self, msg, irc):
    '''Hooks this method to save when a user
    was last seen.
    '''
    if not hasattr(irc, '_seend'):
      irc._seend = {}

    # Don't save info for PMs
    if irc.sender == irc.channel:
      return False

    # Check for the size
    if self.totalSeen(irc) >= self.max_seen:
        self.deleteOldestN(self.max_seen / 2, irc)

    if irc.channel in irc._seend:
      irc._seend[irc.channel][irc.sender] = (datetime.utcnow(), msg)
    else:
      irc._seend[irc.channel] = {irc.sender: (datetime.utcnow(), msg)}

    self.saveSeenDict(irc)

  def loadSeenDict(self, irc):
    '''Load the pickled seend from the
    bot's last run.
    '''
    if not os.path.exists(self.pickle_path):
        if not hasattr(irc, '_seend'):
            irc._seend = {}
        return

    with open(self.pickle_path, 'rb') as pf:
        irc._seend = pickle.loads(zlib.decompress(pf.read()))

  def saveSeenDict(self, irc):
    '''Save the seen dict to the pickled file.
    '''
    with open(self.pickle_path, 'wb+') as pf:
        pf.write(zlib.compress(pickle.dumps(irc._seend)))

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

    # Get the datetime and the relative delta
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

  def totalSeen(self, irc):
    '''Return the total seen messages.
    '''
    if not hasattr(irc, '_seend'):
        return 0

    total = sum(map(len, irc._seend.values()))
    return total
