# -*- coding: utf-8 -*-

from twisted.python import log

import plugins.PluginBase as pb

class Commands(pb.CommandPlugin):
  def __init__(self, conf):
    super(Commands, self).__init__(conf)

  def commands(self):
    return { 'commands': self.listCommands
           , 'help': self.getHelp
           }

  def getHelp(self, args, irc):
    '''help [command] returns usage/help for a given command
    '''
    if not args:
        return self.help(u'help')

    if args[0] not in irc.fact.commands:
        return u'[Error]: {} is not a supported command'.format(args[0])
    else:
        return irc.fact.commands[args[0]].im_self.help(args[0])

  def listCommands(self, args, irc):
    '''commands [plugin] 
    returns a CSV list of all plugins or all 
    supported commands for that plugin
    '''
    # Error checking
    if not args:
      return u', '.join(sorted(irc.fact.plugins.keys()))

    if not args[0] in irc.fact.plugins:
      return u'[Error]: {} is not a supported plugin'.format(args[0])

    # Commands for a given plugin
    return u', '.join(sorted(irc.fact.plugins[args[0]].commands().keys()))
