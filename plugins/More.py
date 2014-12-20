# -*- coding: utf-8 -*-

from twisted.python import log

import plugins.PluginBase as pb
from utils.utf8 import encode

class More(pb.CommandPlugin):
  def __init__(self, conf):
    super(More, self).__init__(conf)

  def commands(self):
    return { 'more': self.more
           }

  def more(self, args, irc):
    if not irc._mored.get(irc.sender):
      return 

    lines = irc._mored[irc.sender]
    line = lines.pop(0)
    suffix = u' \x02({} more messages)\x02'.\
              format(len(lines)) if lines \
                else u''

    log.msg('more: {}'.format(line))
    irc.msg(irc.sender if irc.pm else irc.channel,
                          encode(u'{}{}'.format(line, suffix)))
