# -*- coding: utf-8 -*-
import cPickle as pickle
from datetime import datetime
import os
import zlib

from twisted.python import log

import plugins.PluginBase as pb
from utils.utf8 import encode

class Tell(pb.CommandPlugin):
  def __init__(self, conf):
    super(Tell, self).__init__(conf)

  def commands(self):
    return { 'tell': self.tell
           }

  def loadTellDict(self, irc):
    '''Load the tell dict from disk.
    '''
    if not os.path.exists(self.pickle_path):
        if not hasattr(irc, '_telld'):
            irc._telld = {}
        return

    with open(self.pickle_path, 'rb') as pf:
        irc._telld = pickle.loads(zlib.decompress(pf.read()))

  def saveTellDict(self, irc):
    '''Save the tell dict to disk.
    '''
    if not hasattr(irc, '_telld'):
        return

    with open(self.pickle_path, 'wb') as pf:
        pf.write(zlib.compress(pickle.dumps(irc._telld)))

  def tell(self, args, irc):
    '''(tell nickname message) --
    Tell a user something for later. Only one
    message is queued per nick. For the message to
    arrive, the nick must join a channel the bot is
    on. Does not work if the user is currently online.
    '''
    if len(args) < 2:
      return u'[Error]: tell [nickname] [message]'

    # Create the telld if it doesn't exist
    if not hasattr(irc, '_telld'):
      # For telling users messages
      # Maps a nickname to the text
      # to tell them
      irc._telld = {}

    # Save the nick, sender, and msg to the telld
    nick, msg = args[0], u' '.join(args[1:])
    irc._telld[nick] = (irc.sender, msg, datetime.utcnow())

    # Save the telld to disk
    self.saveTellDict(irc)

    # Check to see if the user is online
    irc._tell_check = (irc.sender, nick)
    irc.who_reply = (None, args[0])
    irc.sendLine('WHO {}'.format(nick))
